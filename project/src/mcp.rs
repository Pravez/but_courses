#![allow(dead_code)]
use std::sync::Arc;

use rmcp::{
    ErrorData as McpError, RoleServer, ServerHandler,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::*,
    schemars,
    service::RequestContext,
    tool, tool_handler, tool_router,
};
use sqlx::{AnyPool, Error, PgPool, Row};
use sqlx::postgres::PgRow;
use tokio::sync::Mutex;

#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
pub struct StructRequest {
    pub a: i32,
    pub b: i32,
}

#[derive(sqlx::FromRow)]
struct TableRecord {
    table_name: String,
    column_name: String,
    data_type: String,
}

#[derive(Debug, serde::Deserialize, schemars::JsonSchema)]
pub struct QueryRequest {
    pub query: String,
}

#[derive(Clone)]
pub struct Counter {
    tool_router: ToolRouter<Counter>,
    pool: PgPool,
}

#[tool_router]
impl Counter {
    #[allow(dead_code)]
    pub fn new(pool: PgPool) -> Self {
        Self {
            tool_router: Self::tool_router(),
            pool,
        }
    }

    #[tool(description = "Get the database schema")]
    async fn get_database_schema(&self) -> Result<CallToolResult, McpError> {
        let schema = sqlx::query_as::<_, TableRecord>(
            "SELECT
    table_name,
    column_name,
    data_type
FROM
    information_schema.columns
WHERE
    table_name = ANY('{classes, courses, enrollments, students}'::text[])
ORDER BY table_name;",
        )
        .fetch_all(&self.pool)
        .await
        .unwrap();

        Ok(CallToolResult::success(vec![Content::text(format!(
            "## Database schema \n\n{}",
            schema
                .iter()
                .map(|r| format!("{}: {} ({})", r.table_name, r.column_name, r.data_type))
                .collect::<Vec<String>>()
                .join("\n")
        ))]))
    }

    #[tool(description = "Execute a SQL query")]
    async fn execute_query(&self, Parameters(QueryRequest { query }): Parameters<QueryRequest>) -> Result<CallToolResult, McpError> {
        let rows = match sqlx::query(&query).fetch_all(&self.pool).await {
            Ok(r) => r,
            Err(_) => return Err(McpError::invalid_request(format!("Invalid query: {}", query), None)),
        };
        Ok(CallToolResult::success(vec![Content::text(format!(
            "## Query result \n\n{}",
            rows.iter().map(|r| format!("{:?}", r)).collect::<Vec<String>>().join("\n")
        ))]))
    }
}

#[tool_handler]
impl ServerHandler for Counter {
    async fn initialize(
        &self,
        _request: InitializeRequestParam,
        context: RequestContext<RoleServer>,
    ) -> Result<InitializeResult, McpError> {
        if let Some(http_request_part) = context.extensions.get::<axum::http::request::Parts>() {
            let initialize_headers = &http_request_part.headers;
            let initialize_uri = &http_request_part.uri;
            tracing::info!(?initialize_headers, %initialize_uri, "initialize from http server");
        }
        Ok(self.get_info())
    }

    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            protocol_version: ProtocolVersion::V_2024_11_05,
            capabilities: ServerCapabilities::builder()
                .enable_tools()
                .build(),
            server_info: Implementation::from_build_env(),
            instructions: Some("This server provides counter tools and prompts. Tools: increment, decrement, get_value, say_hello, echo, sum. Prompts: example_prompt (takes a message), counter_analysis (analyzes counter state with a goal).".to_string()),
        }
    }
}
