/******************************************************************************
 * Copyright (c) 2024, Tri Dao.
 ******************************************************************************/

#pragma once

#include "cute/tensor.hpp"

#include "cutlass/cutlass.h"
#include "cutlass/layout/layout.h"
#include <cutlass/numeric_types.h>

// #define DEBUG_POWER_FWD 1

using namespace cute;

template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, typename elem_type=cutlass::half_t>
struct Power_kernel_traits {

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
    using Element = elem_type;
    static constexpr bool Has_cp_async = true;
#else
    using Element = cutlass::half_t;
    static constexpr bool Has_cp_async = false;
#endif

    using ElementAccum = float;
    using index_t = int64_t;

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 800
    using MMA_Atom_Arch = std::conditional_t<
        std::is_same_v<elem_type, cutlass::half_t>,
        MMA_Atom<SM80_16x8x16_F32F16F16F32_TN>,
        MMA_Atom<SM80_16x8x16_F32BF16BF16F32_TN>
    >;
#else
    using MMA_Atom_Arch = MMA_Atom<SM75_16x8x8_F32F16F16F32_TN>;
#endif

#if defined(__CUDA_ARCH__) &&  __CUDA_ARCH__ >= 750
    using SmemCopyAtom = Copy_Atom<SM75_U32x4_LDSM_N, elem_type>;
    using SmemCopyAtomTransposed = Copy_Atom<SM75_U16x8_LDSM_T, elem_type>;
#else
    using SmemCopyAtom = Copy_Atom<DefaultCopy, elem_type>;
    using SmemCopyAtomTransposed = Copy_Atom<DefaultCopy, elem_type>;
#endif
};

// If Share_Q_K_smem is true, that forces Is_Q_in_regs to be true
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_, bool Is_Q_in_regs_=false, typename elem_type=cutlass::half_t,
         typename Base=Power_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
struct Power_fwd_kernel_traits : public Base {
    using Element = typename Base::Element;
    using ElementAccum = typename Base::ElementAccum;
    using index_t = typename Base::index_t;
    static constexpr bool Has_cp_async = Base::Has_cp_async;
    using SmemCopyAtom = typename Base::SmemCopyAtom;
    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;

    static constexpr bool Is_Q_in_regs = Is_Q_in_regs_;

    // The number of threads.
    static constexpr int kNWarps = kNWarps_;
    static constexpr int kNThreads = kNWarps * 32;

    static constexpr int kBlockM = kBlockM_;
    static constexpr int kBlockN = kBlockN_;
    static constexpr int kHeadDim = kHeadDim_;
    static_assert(kHeadDim % 32 == 0);
    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;

    using TiledMma = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<kNWarps>,_1,_1>>,  // 4x1x1 or 8x1x1 thread group
        Tile<Int<16 * kNWarps>, _16, _16>>;

    using SmemLayoutAtomQ = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    // This has to be kBlockKSmem, using kHeadDim gives wrong results for d=128
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutQ = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockM>, Int<kHeadDim>>{}));

    using SmemLayoutKV = decltype(tile_to_shape(
        SmemLayoutAtomQ{},
        Shape<Int<kBlockN>, Int<kHeadDim>>{}));

    // https://github.com/ColfaxResearch/cutlass-kernels/blob/a222587e6d59b93ba704853d3946fb686d8b8892/src/fmha/fmha_forward.cu#L434
    using SmemLayoutVtransposed = decltype(
        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
    using SmemLayoutVtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutVtransposed{}));

    using SmemLayoutAtomO = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<Int<8>, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutO = decltype(tile_to_shape(
        SmemLayoutAtomO{},
        Shape<Int<kBlockM>, Int<kHeadDim>>{}));
    using SmemLayoutNorm = Layout<Shape<Int<kBlockM>>>;
    using SmemLayoutGQ = Layout<Shape<Int<kBlockM>>>;
    using SmemLayoutGK = Layout<Shape<Int<kBlockN>>>;
    using SmemLayoutP = Layout<Shape<Int<kBlockM>, Int<kBlockN>>>;
    using SmemLayoutRowmax = Layout<Shape<Int<kBlockM>>>;

    using SmemCopyAtomO = Copy_Atom<DefaultCopy, Element>;
    using SmemCopyAtomOaccum = Copy_Atom<DefaultCopy, ElementAccum>;

    static constexpr int kSmemQSize = size(SmemLayoutQ{}) * sizeof(Element);
    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
    static constexpr int kSmemLogGSize = (size(SmemLayoutGQ{}) + size(SmemLayoutGK{})) * sizeof(float);
    static constexpr int kSmemPSize = size(SmemLayoutP{}) * sizeof(ElementAccum);
#if DEBUG_POWER_FWD
    static constexpr int kSmemSize = Is_Q_in_regs ? (kSmemLogGSize + std::max(kSmemQSize, kSmemKVSize) + kSmemPSize) : (kSmemQSize + kSmemKVSize + kSmemLogGSize + kSmemPSize);
#else
    static constexpr int kSmemSize = Is_Q_in_regs ? (kSmemLogGSize + std::max(kSmemQSize, kSmemKVSize)) : (kSmemQSize + kSmemKVSize + kSmemLogGSize);
#endif


    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
    // Using kBlockKSmem here is 6-10% faster than kBlockKGmem for d=128 because of bank conflicts.
    // For example, for d=128, smem is split into 2 "pages", each page takes care of columns
    // 0-63 and 64-127. If we have 16 threads per row for gmem read, when we write to smem,
    // thread 0 - 7 will write to the first page and thread 8 - 15 will write to the second page,
    // to the same banks.
    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
                                  Stride<Int<kGmemThreadsPerRow>, _1>>;

    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
    // from the same address by the same threadblock. This is slightly faster.
    using Gmem_copy_struct = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
        DefaultCopy
    >;

    using GmemTiledCopyQKV = decltype(
        make_tiled_copy(Copy_Atom<Gmem_copy_struct, Element>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read

    // unfortunately we have to polute L1 cache by using CACHEALWAYS because CACHEGLOBAL
    // only supports 128-bit loads, see https://github.com/NVIDIA/cutlass/issues/1768
    using Gmem_copy_struct_float = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<uint128_t>, 
        DefaultCopy
    >;

    using GmemTiledCopyLogG = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint32_t>, float>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));

    using GmemTiledCopyO = decltype(
        make_tiled_copy(Copy_Atom<AutoVectorizingCopy, Element>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per store

    using GmemLayoutAtomOaccum = std::conditional_t<
        kBlockKSmem == 32,
        Layout<Shape <_16, _8>,  // Thread layout, 8 threads per row
               Stride< _8, _1>>,
        Layout<Shape <_8, _16>,  // Thread layout, 16 threads per row
               Stride< _16, _1>>
    >;
    using GmemTiledCopyOaccum = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, ElementAccum>{},
                        GmemLayoutAtomOaccum{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store
    using GmemLayoutAtomRotcossin = GmemLayoutAtom;
    using GmemTiledCopyRotcossin = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint64_t>, Element>{},
                        GmemLayoutAtomRotcossin{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per load
    using GmemTiledCopyRotcossinCont = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, Element>{},
                        GmemLayoutAtomRotcossin{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per load
    using GmemTiledCopyNorm = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, ElementAccum>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));  // Val layout, 1 val per load
    using GmemTiledCopyRowmax = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, float>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));  // Val layout, 1 val per load
};

// Is_V_in_regs is an option to reduce smem usage, but will increase register pressue. (only effective for dKdV)
// No_double_buffer is another option to reduce smem usage, but will slow things down.
template<int kHeadDim_, int kBlockM_, int kBlockN_, int kNWarps_,
         int AtomLayoutMSdP_=1, int AtomLayoutNdKV_=2, int AtomLayoutMdQ_=2,
         bool Is_V_in_regs_=false, bool No_double_buffer_=false, typename elem_type=cutlass::half_t,
         typename Base=Power_kernel_traits<kHeadDim_, kBlockM_, kBlockN_, kNWarps_, elem_type> >
struct Power_bwd_kernel_traits : public Base {
    using Element = typename Base::Element;
    using ElementAccum = typename Base::ElementAccum;
    using index_t = typename Base::index_t;
    static constexpr bool Has_cp_async = Base::Has_cp_async;
    using SmemCopyAtom = typename Base::SmemCopyAtom;
    using SmemCopyAtomTransposed = typename Base::SmemCopyAtomTransposed;

    static constexpr bool Is_V_in_regs = Is_V_in_regs_;
    static constexpr bool No_double_buffer = No_double_buffer_;

    // The number of threads.
    static constexpr int kNWarps = kNWarps_;
    static constexpr int kNThreads = kNWarps * 32;

    static constexpr int kBlockM = kBlockM_;
    static constexpr int kBlockN = kBlockN_;
    static constexpr int kHeadDim = kHeadDim_;
    static_assert(kHeadDim % 32 == 0);
    static constexpr int kBlockKSmem = kHeadDim % 64 == 0 ? 64 : 32;
    static constexpr int kBlockKGmem = kHeadDim % 128 == 0 ? 128 : (kHeadDim % 64 == 0 ? 64 : 32);
    static constexpr int kSwizzle = kBlockKSmem == 32 ? 2 : 3;

    static constexpr int AtomLayoutMSdP = AtomLayoutMSdP_;
    static constexpr int AtomLayoutNdKV = AtomLayoutNdKV_;
    static constexpr int AtomLayoutMdQ = AtomLayoutMdQ_;
    static_assert(kNWarps % AtomLayoutMSdP == 0);
    static_assert(kNWarps % AtomLayoutNdKV == 0);
    static_assert(kNWarps % AtomLayoutMdQ == 0);

    using TiledMmaSdP = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutMSdP>, Int<kNWarps / AtomLayoutMSdP>, _1>>,
        Tile<Int<16 * AtomLayoutMSdP>, Int<16 * kNWarps / AtomLayoutMSdP>, _16>>;

    using TiledMmadKV = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutNdKV>, Int<kNWarps / AtomLayoutNdKV>, _1>>,
        Tile<Int<16 * AtomLayoutNdKV>, Int<16 * kNWarps / AtomLayoutNdKV>, _16>>;

    using TiledMmadQ = TiledMMA<
        typename Base::MMA_Atom_Arch,
        Layout<Shape<Int<AtomLayoutMdQ>, Int<kNWarps / AtomLayoutMdQ>, _1>>,  // 2x4x1 or 4x2x1 thread group
        Tile<Int<16 * AtomLayoutMdQ>, Int<16 * kNWarps / AtomLayoutMdQ>, _16>>;

    using SmemLayoutAtomQdY = decltype(composition(Swizzle<kSwizzle, 3, 3>{},
                                                   Layout<Shape<_8, Int<kBlockKSmem>>,
                                                          Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutQdY = decltype(tile_to_shape(
        SmemLayoutAtomQdY{},
        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
    using SmemLayoutQdYtransposed = decltype(composition(SmemLayoutQdY{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockM>>{}, GenRowMajor{})));
    using SmemLayoutQdYtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutQdYtransposed{}));

    // TODO (sean): swizzle this
    using SmemLayoutdy = Layout<Shape<Int<kBlockM>>, Stride<_1>>;

    using SmemLayoutAtomKV = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutKV = decltype(tile_to_shape(
        SmemLayoutAtomKV{},
        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));

    using SmemLayoutGQ = Layout<Shape<Int<kBlockM>>>;
    using SmemLayoutGK = Layout<Shape<Int<kBlockN>>>;
    using SmemLayoutRowmax = Layout<Shape<Int<kBlockM>>>;

    using SmemLayoutKtransposed = decltype(
        composition(SmemLayoutKV{}, make_layout(Shape<Int<kHeadDim>, Int<kBlockN>>{}, GenRowMajor{})));
    using SmemLayoutKtransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutKtransposed{}));

    // TODO: generalize to other values of kBlockN
    // TODO: what should be the Swizzle here? 3 is faster than 1, and 1 is faster than 2
    // static constexpr int kPBlockN = kBlockN;
    // Temporarily disabling this for hdim 256 on sm86 and sm89
    // static_assert(kBlockN >= 64);
    static_assert(kBlockN >= 32);
    // TD [2023-03-19]: Idk why kPBlockN = 16 and kSwizzlePdS=3 is the fastest.
    static constexpr int kPBlockN = kBlockN >= 64 ? 64 : 32;
    static_assert(kPBlockN == 16 || kPBlockN == 32 || kPBlockN == 64);
    // static constexpr int kSwizzlePdS = kPBlockN == 16 ? 1 : (kPBlockN == 32 ? 2 : 3);
    static constexpr int kSwizzlePdS = 3;
    using SmemLayoutAtomPdS = decltype(
        composition(Swizzle<kSwizzlePdS, 3, 3>{},
                    Layout<Shape<Int<kBlockM>, Int<kPBlockN>>,
                           Stride<Int<kPBlockN>, _1>>{}));
    using SmemLayoutPdS = decltype(tile_to_shape(
        SmemLayoutAtomPdS{},
        make_shape(Int<kBlockM>{}, Int<kBlockN>{})));
    using SmemLayoutPdStransposed = decltype(
        composition(SmemLayoutPdS{}, make_layout(Shape<Int<kBlockN>, Int<kBlockM>>{}, GenRowMajor{})));
    using SmemLayoutPdStransposedNoSwizzle = decltype(get_nonswizzle_portion(SmemLayoutPdStransposed{}));

    using SmemCopyAtomPdS = Copy_Atom<DefaultCopy, elem_type>;

    using SmemLayoutAtomdKV = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutdKV = decltype(tile_to_shape(
        SmemLayoutAtomdKV{},
        make_shape(Int<kBlockN>{}, Int<kHeadDim>{})));
    using SmemCopyAtomdKV = Copy_Atom<DefaultCopy, elem_type>;

    using SmemLayoutAtomdQ = decltype(
        composition(Swizzle<kSwizzle, 3, 3>{},
                    Layout<Shape<_8, Int<kBlockKSmem>>,
                           Stride<Int<kBlockKSmem>, _1>>{}));
    using SmemLayoutdQ = decltype(tile_to_shape(
        SmemLayoutAtomdQ{},
        make_shape(Int<kBlockM>{}, Int<kHeadDim>{})));
    using SmemCopyAtomdQ = Copy_Atom<DefaultCopy, elem_type>;

    // Smem for dKdV kernel
    static constexpr int kSmemQdYSize = size(SmemLayoutQdY{}) * (No_double_buffer ? 2 : 3) * sizeof(Element);
    static constexpr int kSememdySize = size(SmemLayoutdy{}) * sizeof(float);
    static constexpr int kSmemKSize = size(SmemLayoutKV{}) * sizeof(Element);
    static constexpr int kSmemVSize = size(SmemLayoutKV{}) * sizeof(Element);
    static constexpr int kSmemKVSize = size(SmemLayoutKV{}) * 2 * sizeof(Element);
    static constexpr int kSmemdSSize = size(SmemLayoutPdS{}) * sizeof(Element);
    static constexpr int kSmemPSize = size(SmemLayoutPdS{}) * sizeof(Element);
    static_assert(kSmemdSSize == kSmemPSize, "kSmemdSSize must be equal to kSmemPSize");
    static constexpr int kSmemdQSize = size(SmemLayoutdQ{}) * sizeof(Element);
    static constexpr int kSmemLogGQSize = size(SmemLayoutGQ{}) * sizeof(float);
    static constexpr int kSmemLogGSize = (size(SmemLayoutGQ{}) + size(SmemLayoutGK{})) * sizeof(float);
    static constexpr int kSmemRowmaxSize = size(SmemLayoutRowmax{}) * sizeof(float);
    static constexpr int kSmemSize = kSmemQdYSize + kSememdySize + (!Is_V_in_regs ? kSmemKVSize + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize) : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemdSSize + std::max(kSmemPSize, kSmemdQSize)));
    static constexpr int kSmemSize1colblock = kSmemQdYSize + kSememdySize + kSmemLogGSize + (!Is_V_in_regs ? kSmemKVSize + kSmemPSize : std::max(kSmemKVSize, kSmemKVSize / 2 + kSmemPSize));
    static constexpr int kSmemSize1colblock_dq_dk_dv_gating = kSmemQdYSize + kSememdySize + kSmemKSize + (Is_V_in_regs ? (std::max(kSmemVSize, kSmemdSSize + kSmemPSize + kSmemLogGSize + kSmemRowmaxSize)) : (kSmemVSize + kSmemdSSize + kSmemPSize + kSmemLogGSize + kSmemRowmaxSize));
    static constexpr int kSmemSize1colblock_dq_dk_dv_no_gating = kSmemQdYSize + kSememdySize + kSmemKSize + (Is_V_in_regs ? (std::max(kSmemVSize, kSmemdSSize + kSmemPSize + kSmemRowmaxSize)) : (kSmemVSize + kSmemdSSize + kSmemPSize + kSmemRowmaxSize));

    // Smem for dQ kernel
    static constexpr int kSmemQSize = size(SmemLayoutQdY{}) * sizeof(Element);
    static constexpr int kSmemdYSize = size(SmemLayoutQdY{}) * sizeof(Element);
    static constexpr int kSmemKSize_dQ = (No_double_buffer ? 1 : 2) * size(SmemLayoutKV{}) * sizeof(Element);
    static constexpr int kSmemVSize_dQ = size(SmemLayoutKV{}) * sizeof(Element);
    static constexpr int kSmemSize1rowblock = kSmemQSize + kSmemdYSize + kSememdySize + kSmemLogGSize + kSmemKSize_dQ + kSmemVSize_dQ + kSmemdSSize;

    static constexpr int kGmemElemsPerLoad = sizeof(cute::uint128_t) / sizeof(Element);
    static_assert(kHeadDim % kGmemElemsPerLoad == 0, "kHeadDim must be a multiple of kGmemElemsPerLoad");
    // Using kBlockKSmem instead of kHeadDim here to avoid bank conflicts, but doesn't seem
    // to affect speed in practice.
    static constexpr int kGmemThreadsPerRow = kBlockKSmem / kGmemElemsPerLoad;
    static_assert(kNThreads % kGmemThreadsPerRow == 0, "kNThreads must be a multiple of kGmemThreadsPerRow");
    using GmemLayoutAtom = Layout<Shape <Int<kNThreads / kGmemThreadsPerRow>, Int<kGmemThreadsPerRow>>,
                                  Stride<Int<kGmemThreadsPerRow>, _1>>;

    // We use CACHEGLOBAL instead of CACHEALWAYS for both Q and K/V, since we won't be reading
    // from the same address by the same threadblock. This is slightly faster.
    using Gmem_copy_struct = std::conditional_t<
        Has_cp_async,
        SM80_CP_ASYNC_CACHEGLOBAL<cute::uint128_t>,
        DefaultCopy
    >;
    using GmemTiledCopyQKV = decltype(
        make_tiled_copy(Copy_Atom<Gmem_copy_struct, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape<_1, _8>>{}));  // Val layout, 8 vals per read
    using GmemTiledCopydO = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store

    using GmemTiledCopyLogG = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint32_t>, float>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));

    using GmemTiledCopydy = decltype(make_tiled_copy(Copy_Atom<UniversalCopy<uint32_t>, float>{},
                                                     Layout<Shape<Int<kNThreads>>>{},
                                                     Layout<Shape<_1>>{}));
    using GmemTiledCopydKV = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint128_t>, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
    using GmemTiledCopydQ = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint128_t>, elem_type>{},
                        GmemLayoutAtom{},
                        Layout<Shape < _1, _8>>{}));  // Val layout, 8 vals per store
    using GmemLayoutAtomdQaccum = std::conditional_t<
        kBlockKSmem == 32,
        Layout<Shape <_32, _8>,  // Thread layout, 8 threads per row
               Stride< _8, _1>>,
        Layout<Shape <_16, _16>,  // Thread layout, 16 threads per row
               Stride< _16, _1>>
    >;
    using GmemTiledCopydQaccum = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint128_t>, ElementAccum>{},
                        GmemLayoutAtomdQaccum{},
                        Layout<Shape < _1, _4>>{}));  // Val layout, 4 vals per store

    using GmemTiledCopydQaccumAtomicAdd = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, ElementAccum>{},
                        Layout<Shape <_8, _32>,  // Thread layout, 8 threads per row
                               Stride<_32, _1>>{},
                        Layout<Shape < _1, _1>>{}));  // Val layout, 1 val per store

    using GmemTiledCopydLogG = decltype(
        make_tiled_copy(Copy_Atom<UniversalCopy<uint32_t>, float>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));

    using GmemTiledCopyRowmax = decltype(
        make_tiled_copy(Copy_Atom<DefaultCopy, float>{},
                        Layout<Shape<Int<kNThreads>>>{},
                        Layout<Shape<_1>>{}));  // Val layout, 1 val per load

    using GmemTiledCopydLogGAtomicAdd = GmemTiledCopydLogG;

    friend std::ostream& operator<<(std::ostream& os, const Power_bwd_kernel_traits& traits) {
        os << "Power_bwd_kernel_traits<"
           << "kHeadDim=" << traits.kHeadDim << ", "
           << "kBlockM=" << traits.kBlockM << ", "
           << "kBlockN=" << traits.kBlockN << ", "
           << "kNWarps=" << traits.kNWarps << ", "
           << "AtomLayoutMSdP=" << traits.AtomLayoutMSdP << ", "
           << "AtomLayoutNdKV=" << traits.AtomLayoutNdKV << ", "
           << "AtomLayoutMdQ=" << traits.AtomLayoutMdQ << ", "
           << "Is_V_in_regs=" << std::boolalpha << traits.Is_V_in_regs << ", "
           << "No_double_buffer=" << traits.No_double_buffer << ">";
        return os;
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////
