FROM rust:1-slim

COPY ./ ./

RUN cargo build --release

CMD ["./target/release/but_mcp"]