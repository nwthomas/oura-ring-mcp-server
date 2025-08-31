# Oura Ring MCP Server

A model context protocol (MCP) implementation wrapping calls to the Oura Ring API.

## Oura Ring API Notes

Oura Ring limits users to 5,000 requests per 5 minute period, but they say they have not had any users hit rate limits with webhook properly implemented.

Different data has different sync policies for them:
- Sleep data only syncs when users open the app
- Daily activity and stress, for instance, sync in the background

In order to use this MCP server, you will need to register with the Oura Ring developer portal and get your own keys to plug into a `.env` file (copied over from the `.env.example`).

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Oura Ring API Documentation](https://cloud.ouraring.com/v2/docs)
