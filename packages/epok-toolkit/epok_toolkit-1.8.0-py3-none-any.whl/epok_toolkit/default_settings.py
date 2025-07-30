# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_DEFAULT_FROM_EMAIL = "no-reply@epok.ai"
EMAIL_HOST_USER = "no-reply@epok.ai"
EMAIL_HOST_PASSWORD = "your-email-password"


# Configuración de whatsApp
API_KEY = "your-whatsapp-api-key"
INSTANCE = "instance-id"
SERVER_URL = "https://your-server-url.com/"