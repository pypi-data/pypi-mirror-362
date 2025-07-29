# Connect

Methods:

- <code title="post /connect">client.connect.<a href="./src/metis/resources/connect.py">initialize</a>() -> object</code>

# Reconnect

Methods:

- <code title="post /reconnect">client.reconnect.<a href="./src/metis/resources/reconnect.py">reconnect</a>() -> object</code>

# OAuth

Methods:

- <code title="delete /oauth/session/{session_id}">client.oauth.<a href="./src/metis/resources/oauth.py">cleanup_session</a>(session_id) -> object</code>
- <code title="get /oauth/auth-header/{session_id}/{provider}">client.oauth.<a href="./src/metis/resources/oauth.py">get_auth_header</a>(provider, \*, session_id) -> object</code>
- <code title="get /oauth/callback">client.oauth.<a href="./src/metis/resources/oauth.py">handle_callback</a>(\*\*<a href="src/metis/types/oauth_handle_callback_params.py">params</a>) -> object</code>
- <code title="post /oauth/initiate">client.oauth.<a href="./src/metis/resources/oauth.py">initiate</a>(\*\*<a href="src/metis/types/oauth_initiate_params.py">params</a>) -> object</code>
- <code title="get /oauth/status/{session_id}">client.oauth.<a href="./src/metis/resources/oauth.py">retrieve_status</a>(session_id) -> object</code>
- <code title="get /oauth/test-config">client.oauth.<a href="./src/metis/resources/oauth.py">test_config</a>() -> object</code>

# Mcp

Methods:

- <code title="get /mcp/debug/{session_id}">client.mcp.<a href="./src/metis/resources/mcp/mcp.py">get_debug_info</a>(session_id) -> object</code>

## OAuth

Methods:

- <code title="get /mcp/oauth/callback">client.mcp.oauth.<a href="./src/metis/resources/mcp/oauth.py">handle_callback</a>() -> object</code>

# Sessions

Methods:

- <code title="get /sessions/{session_id}/tools">client.sessions.<a href="./src/metis/resources/sessions.py">list_tools</a>(session_id) -> object</code>
- <code title="post /sessions/{session_id}/message">client.sessions.<a href="./src/metis/resources/sessions.py">send_message</a>(session_id) -> object</code>
- <code title="get /sessions/{session_id}/stream">client.sessions.<a href="./src/metis/resources/sessions.py">stream_response</a>(session_id) -> object</code>

# Health

Methods:

- <code title="get /health">client.health.<a href="./src/metis/resources/health.py">check</a>() -> object</code>

# Test

Methods:

- <code title="get /test/postmessage">client.test.<a href="./src/metis/resources/test.py">post_message</a>() -> object</code>
