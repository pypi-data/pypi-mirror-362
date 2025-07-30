FROM mstorsjo/llvm-mingw:20250709 as build
WORKDIR /build
RUN wget https://github.com/llvm/llvm-project/releases/download/llvmorg-17.0.6/llvm-project-17.0.6.src.tar.xz
RUN tar \
    --no-same-owner \
    --no-same-permissions \
    --no-overwrite-dir \
    --exclude="llvm-project-17.0.6.src/clang/test" \
    --exclude="llvm-project-17.0.6.src/libclc" \
    -xf llvm-project-17.0.6.src.tar.xz

RUN mkdir llvm-native-build
WORKDIR /build/llvm-native-build
ENV TARGET="host"
RUN cmake -S /build/llvm-project-17.0.6.src/llvm \
    -G "Ninja" \
    -DCMAKE_INSTALL_PREFIX=/opt/llvm-mingw/lib/llvm-17 \
    -DLLVM_TARGETS_TO_BUILD=${TARGET} \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_BUILD_TOOLS=OFF \
    -DCMAKE_BUILD_TYPE=Release
RUN cmake --build . --target all
RUN cmake --build . --target install

WORKDIR /build
RUN wget https://github.com/EnzymeAD/Enzyme/archive/refs/tags/v0.0.185.tar.gz
RUN tar --no-same-owner --no-same-permissions --no-overwrite-dir -xf v0.0.185.tar.gz
WORKDIR /build/enzyme-native-build
RUN cmake -S /build/Enzyme-0.0.185/enzyme \
    -G "Ninja" \
    -DCMAKE_INSTALL_PREFIX=/opt/llvm-mingw/lib/llvm-17 \
    -DLLVM_DIR=/opt/llvm-mingw/lib/llvm-17 \
    -DENZYME_STATIC_LIB=ON \
    -DENZYME_EXTERNAL_SHARED_LIB=ON \
    -DENZYME_CLANG=OFF \
    -DCMAKE_BUILD_TYPE=Release
RUN cmake --build . --target enzyme-tblgen

RUN mkdir llvm-build
WORKDIR /build/llvm-build
ENV TARGET=X86
ENV PROCESSOR=x86_64
ENV ARCH=x86_64-w64-mingw32
RUN cmake -S /build/llvm-project-17.0.6.src/llvm \
    -G "Ninja" \
    -DCMAKE_SYSTEM_NAME=Windows \
    -DCMAKE_SYSTEM_PROCESSOR=$PROCESSOR \
    -DCMAKE_PREFIX_PATH=/opt/llvm-mingw/$ARCH \
    -DCMAKE_C_COMPILER=/opt/llvm-mingw/bin/$ARCH-clang \
    -DCMAKE_C_COMPILER_TARGET=$ARCH \
    -DCMAKE_CXX_COMPILER=/opt/llvm-mingw/bin/$ARCH-clang++ \
    -DCMAKE_CXX_COMPILER_TARGET=$ARCH \
    -DCMAKE_FIND_ROOT_PATH=/opt/llvm-mingw/$ARCH \
    -DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
    -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY \
    -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY \
    -DCMAKE_INSTALL_PREFIX=/opt/llvm-mingw/$ARCH/llvm-17 \
    -DLLVM_BUILD_LLVM_DYLIB=ON \
    -DLLVM_TARGETS_TO_BUILD=${TARGET} \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_BUILD_TOOLS=OFF \
    -DCMAKE_BUILD_TYPE=Release
RUN cmake --build . --target all
RUN cmake --build . --target install

WORKDIR /build
RUN wget https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz
RUN tar --no-same-owner --no-same-permissions --no-overwrite-dir -xf gmp-6.3.0.tar.xz
WORKDIR /build/gmp-6.3.0
RUN ./configure --host=$ARCH --prefix=/opt/llvm-mingw/$ARCH/ 
RUN make
RUN make install

WORKDIR /build
RUN wget https://www.mpfr.org/mpfr-current/mpfr-4.2.2.tar.xz
RUN tar --no-same-owner --no-same-permissions --no-overwrite-dir -xf mpfr-4.2.2.tar.xz
WORKDIR /build/mpfr-4.2.2
RUN ./configure --host=$ARCH --prefix=/opt/llvm-mingw/$ARCH/ --enable-static --disable-shared
RUN make
RUN make install

WORKDIR /build/enzyme-build
RUN cmake -S /build/Enzyme-0.0.185/enzyme \
    -G "Ninja" \
    -DCMAKE_SYSTEM_NAME=Windows \
    -DCMAKE_SYSTEM_PROCESSOR=$PROCESSOR \
    -DCMAKE_PREFIX_PATH=/opt/llvm-mingw/$ARCH \
    -DCMAKE_C_COMPILER=/opt/llvm-mingw/bin/$ARCH-clang \
    -DCMAKE_C_COMPILER_TARGET=$ARCH \
    -DCMAKE_CXX_COMPILER=/opt/llvm-mingw/bin/$ARCH-clang++ \
    -DCMAKE_CXX_COMPILER_TARGET=$ARCH \
    -DCMAKE_FIND_ROOT_PATH=/opt/llvm-mingw/$ARCH \
    -DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
    -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY \
    -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY \
    -DBC_LOAD_HEADER=/build/enzyme-native-build/BCLoad/gsl/blas_headers.h \
    -DEnzyme_TABLEGEN=/build/enzyme-native-build/tools/enzyme-tblgen/enzyme-tblgen \
    -DEnzyme_TABLEGEN_EXE=/build/enzyme-native-build/tools/enzyme-tblgen/enzyme-tblgen \
    -DCMAKE_INSTALL_PREFIX=/opt/llvm-mingw/$ARCH/llvm-17 \
    -DLINK_DIRECTORIES=/opt/llvm-mingw/$ARCH/llvm-17/lib \
    -DLLVM_DIR=/opt/llvm-mingw/$ARCH/llvm-17 \
    -DENZYME_STATIC_LIB=ON \
    -DENZYME_EXTERNAL_SHARED_LIB=ON \
    -DENZYME_ENABLE_PLUGINS=OFF \
    -DENZYME_CLANG=OFF \
    -DCMAKE_BUILD_TYPE=Release
RUN cmake --build . --target all
RUN cmake --build . --target install

FROM  mstorsjo/llvm-mingw:20250709

WORKDIR /build
COPY --from=build /opt/llvm-mingw/lib/$ARCH/llvm-17 /opt/llvm-mingw/lib/$ARCH/llvm-17