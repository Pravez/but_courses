use rmcp::transport::sse_server::{SseServer, SseServerConfig};
use sqlx::postgres::PgPoolOptions;
use tracing_subscriber::{
    layer::SubscriberExt,
    util::SubscriberInitExt,
    {self},
};
use crate::counter::Counter;

mod counter;

const BIND_ADDRESS: &str = "127.0.0.1:8000";

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "debug".to_string().into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(database_url.as_str()).await?;


    let ct = SseServer::serve(BIND_ADDRESS.parse()?)
        .await?
        .with_service_directly(move || Counter::new(pool.clone()));

    tokio::signal::ctrl_c().await?;
    ct.cancel();
    Ok(())
}