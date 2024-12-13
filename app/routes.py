from flask import Blueprint, request, jsonify, render_template, current_app, session
import uuid

main = Blueprint('main', __name__)

@main.route('/api/get-conversation')
def get_conversation():
    return jsonify({
        'conversation': session.get('conversation', [])
    })



@main.route('/')
def index():
    # Generate a unique session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['conversation'] = [{
            "role": "user",
            "content": "You are Claude, an AI assistant created by Anthropic. You're helpful, harmless, and honest."
        }]
    return render_template('index.html')


@main.route('/api/chat', methods=['POST'])
def chat():
    try:
        current_app.logger.debug("Received chat request")
        data = request.json
        if not data:
            raise ValueError("No data received")

        conversation = data.get('conversation', [])
        if not conversation:
            raise ValueError("No conversation data")

        current_app.logger.debug(f"Conversation: {conversation}")

        messages = [{"role": m["role"], "content": m["content"]}
                    for m in conversation]

        current_app.logger.debug("Calling Claude API")
        response = current_app.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            messages=messages
        )
        current_app.logger.debug(f"Claude API response: {response}")

        if response.content and isinstance(response.content, list):
            assistant_message = response.content[0].text
        else:
            raise ValueError("Invalid response from Claude API")

        conversation.append({
            "role": "assistant",
            "content": assistant_message
        })
        session['conversation'] = conversation

        return jsonify({"content": assistant_message})
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

