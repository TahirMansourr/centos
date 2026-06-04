import os
from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def check_db_connection():
    # 1. Dynamically read the environment variables we bound earlier
    db_host = os.environ.get('DATABASE_HOST', 'postgresql') 
    db_name = os.environ.get('DB_DATABASE_NAME')   
    db_user = os.environ.get('DB_DATABASE_USER')   
    db_pass = os.environ.get('DB_DATABASE_PASSWORD')

    connection_status = False
    details_message = ""

    # 2. Attempt to open a connection to the relational database
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            connect_timeout=3  # Fast timeout if it can't connect
        )
        conn.close()
        connection_status = True
        details_message = "🎉 SUCCESS! The web application successfully established a secure connection to the relational database."
    except Exception as error:
        connection_status = False
        details_message = f"❌ CONNECTION FAILED: {str(error)}"

    # 3. Simple HTML layout to present nicely in your Windows browser
    html_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenShift Cloud App Status</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f7f9fa; }}
            .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #2d3748; border-bottom: 2px solid #edf2f7; padding-bottom: 10px; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ padding: 8px 0; border-bottom: 1px solid #f7fafc; color: #4a5568; }}
            .status {{ margin-top: 25px; padding: 15px; border-radius: 6px; font-weight: bold; line-height: 1.5; }}
            .success {{ background-color: #c6f6d5; color: #22543d; border-left: 5px solid #38a169; }}
            .failed {{ background-color: #fed7d7; color: #742a2a; border-left: 5px solid #e53e3e; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>App Network Overview</h1>
            <p><strong>Environment Config Bindings:</strong></p>
            <ul>
                <li><strong>Target Host:</strong> {db_host}</li>
                <li><strong>Database Name:</strong> {db_name}</li>
                <li><strong>Username:</strong> {db_user}</li>
            </ul>
            <div class="status {'success' if connection_status else 'failed'}">
                {details_message}
            </div>
        </div>
    </body>
    </html>
    """
    return html_output

if __name__ == '__main__':
    # OpenShift routes internal traffic on port 8080
    app.run(host='0.0.0.0', port=8080)