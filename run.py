from app import app, create_tables
import os

if __name__ == '__main__':
    create_tables()
    port = int(os.environ.get("PORT", 1002))
    app.run(debug=True, host='0.0.0.0', port=port, 
        ssl_context=(r'C:\Certbot\archive\expose.agentsofatom.com\fullchain2.pem',
                    r'C:\Certbot\archive\expose.agentsofatom.com\privkey2.pem'))

# if __name__ == '__main__':
#     create_tables()
#     port = int(os.environ.get("PORT", 1002))
#     app.run(debug=True, host='0.0.0.0', port=port)