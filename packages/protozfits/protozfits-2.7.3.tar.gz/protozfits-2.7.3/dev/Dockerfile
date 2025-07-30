# docker file to build manylinux wheels for the python bindings
FROM quay.io/pypa/manylinux2014_x86_64

RUN ulimit -n 1024 && yum install -y zeromq-devel zlib-devel \
    && yum clean all \
    && rm -rf /var/cache/yum


ENV PROTOBUF_VERSION="3.20.3"

# we need protobuf3 for python3
# passing -O2 dramatically reduces library and thus wheel size

RUN cd /tmp \
	&& curl -L https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protobuf-all-${PROTOBUF_VERSION}.tar.gz | tar xz \
	&& cd protobuf-${PROTOBUF_VERSION} \
	&& ./configure \
	&& make CXXFLAGS="-O2" LDFLAGS="-Wl,-rpath -Wl,'\$\$ORIGIN:\$\$ORIGIN/../lib'" -j \
	&& make install \
	&& cd / \
	&& rm -rf /tmp/protobuf-${PROTOBUF_VERSION} \
	&& readelf -a /usr/local/bin/protoc | grep RPATH \
	&& protoc --version



ADD build_wheels.sh /

RUN mkdir -p /home/wheel && chmod a+rwx /home/wheel
ENV HOME=/home/wheel
ENV PATH="/home/wheel/.local/bin:$PATH"
WORKDIR /home/wheel

CMD /build_wheels.sh
