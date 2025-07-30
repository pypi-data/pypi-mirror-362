"""
notifications/method/email_templates.py
Catálogo central de plantillas de correo con estilo corporativo “morado minimalista”.
Cada plantilla declara las variables que necesita y se renderiza vía EmailTemplate.
"""

from dataclasses import dataclass
from typing import Dict, List


# ---------------------------------------------------------------------------#
# Shared purple‑minimalist wrapper
# ---------------------------------------------------------------------------#
def wrap_html(content: str) -> str:
    """
    Envuelve el bloque `content` en el layout HTML corporativo de Congrats.
    """
    return f"""
    <div style="font-family: Arial, Helvetica, sans-serif; background-color: #f9fafb; padding: 24px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden;">
            <tr>
                <td style="background: #4f46e5; padding: 20px 24px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Congrats 🎉</h1>
                </td>
            </tr>
            
            <tr>
                <td style="padding: 32px 24px;">
                    {content}
                </td>
            </tr>
        </table>
    </div>
    """


# ---------------------------------------------------------------------------#
# Core dataclasses
# ---------------------------------------------------------------------------#
@dataclass(frozen=True)
class RenderedEmail:
    subject: str
    plain: str
    html: str


@dataclass(frozen=True)
class EmailTemplate:
    """
    subject        – Cadena con placeholders, e.g. 'Hola {name}'
    plain_body     – Versión texto plano
    html_body      – HTML completo (usa wrap_html)
    required_vars  – Lista de variables obligatorias
    """
    subject: str
    plain_body: str
    html_body: str
    required_vars: List[str]

    def render(self, context: Dict[str, str]) -> RenderedEmail:
        missing = [v for v in self.required_vars if v not in context]
        if missing:
            raise ValueError(f"Faltan llaves en contexto: {missing}")

        return RenderedEmail(
            subject=self.subject.format(**context),
            plain=self.plain_body.format(**context),
            html=self.html_body.format(**context),
        )


# ---------------------------------------------------------------------------#
# Template catalogue
# ---------------------------------------------------------------------------#
TEMPLATES: Dict[str, EmailTemplate] = {
    "password_reset": EmailTemplate(
        subject="🎉 Restablecimiento de Contraseña – Congrats 🎉",
        plain_body=(
            "¡Hola {name}! 🎉\n\n"
            "Para poner tu fiesta de contraseñas en marcha, haz clic aquí:\n"
            "{reset_link} 🎊\n\n"
            "Si no fuiste tú quien pidió cambio, relájate y ignora este correo. 😉\n\n"
            "¡Nos vemos en la pista de baile!\nEl equipo de Congrats 🥳"
        ),
        html_body=wrap_html(
            "<p style='font-size:16px;'>¡Hola <strong>{name}</strong>! 🎉</p>"
            "<p style='font-size:16px;margin:24px 0;'>"
            "Haz clic en el botón para restablecer tu contraseña y unirte a la celebración:</p>"
            "<p style='text-align:center;margin:24px 0;'>"
            "<a href='{reset_link}' style='display:inline-block;padding:12px 24px;font-size:16px;"
            "color:#ffffff;background-color:#4f46e5;text-decoration:none;border-radius:5px;'>"
            "🔒 Restablecer Contraseña 🎊</a>"
            "</p>"
            "<p style='font-size:16px;'>"
            "Si eso no funciona, copia y pega este enlace en tu navegador:<br>"
            "<span style='word-break:break-all;font-size:14px;'>{reset_link}</span>"
            "</p>"
            "<p style='font-size:16px;margin-top:24px;'>"
            "Si no solicitaste esto, tranquilo, nada cambió. 😌<br><br>"
            "¡A celebrar pronto!<br><em>El equipo de Congrats 🥳</em>"
            "</p>"
        ),
        required_vars=["name", "reset_link"],
    ),

    "welcome": EmailTemplate(
        subject="¡Bienvenido a Congrats, {name}! 🎉🥳",
        plain_body=(
            "¡Hola {name}! 🎈\n\n"
            "Gracias por registrarte en Congrats. Prepárate para la mejor fiesta de eventos. 😎\n\n"
            "¡Nos vemos pronto!\nEl equipo de Congrats 🥳"
        ),
        html_body=wrap_html(
            "<p style='font-size:16px;'>¡Hola <strong>{name}</strong>! 🎈</p>"
            "<p style='font-size:16px;margin:24px 0;'>"
            "Gracias por unirte a <strong>Congrats 🎉</strong>. Prepárate para la mejor fiesta de eventos. 😎"
            "</p>"
            "<p style='font-size:16px;margin-top:24px;'>"
            "¡Nos vemos pronto!<br><em>El equipo de Congrats 🥳</em>"
            "</p>"
        ),
        required_vars=["name"],
    ),
    
    
    "password_reset_success": EmailTemplate(
        subject="🔑 Contraseña restablecida – Congrats 🥳",
        plain_body=(
            "¡Hola {name}! 🔑\n\n"
            "Tu contraseña ya está lista para seguir la fiesta. 🎉\n\n"
            "Si no fuiste tú, ponte alerta. 😉\n\n"
            "Saludos festivos,\nEl equipo de Congrats 🥳"
        ),
        html_body=wrap_html(
            "<p style='font-size:16px;'>¡Hola <strong>{name}</strong>! 🔑</p>"
            "<p style='font-size:16px;margin:24px 0;'>"
            "Tu contraseña ha sido restablecida con éxito. Ahora vuelve a la pista de baile. 🎉"
            "</p>"
            "<p style='font-size:16px;margin-top:24px;'>"
            "Si no fuiste tú, ignora o avísanos. 🤔<br><em>El equipo de Congrats 🥳</em>"
            "</p>"
        ),
        required_vars=["name"],
    ),
    
    
    "ticket_created": EmailTemplate(
        subject="🎫 ¡Tus tickets para {reunion_name} están listos! 🎉",
        plain_body=(
            "¡Hola {name}! 🎟️\n\n"
            "Has comprado {tickets} tickets para “{reunion_name}”. ¡A vivir la experiencia! 🎊\n\n"
            "¡Disfruta al máximo!\nEl equipo de Congrats 🥳"
        ),
        html_body=wrap_html(
            "<p style='font-size:16px;'>¡Hola <strong>{name}</strong>! 🎟️</p>"
            "<p style='font-size:16px;margin:24px 0;'>"
            "Tus {tickets} tickets para <strong>{reunion_name}</strong> están listos. ¡Nos vemos en la fiesta! 🎊"
            "</p>"
            "<p style='font-size:16px;margin-top:24px;'>"
            "¡Que lo disfrutes!<br><em>El equipo de Congrats 🥳</em>"
            "</p>"
        ),
        required_vars=["name", "reunion_name", "tickets"],
    ),
    
    
    "test_app_running": EmailTemplate(
        subject="🚀 Test OK – Congrats 🎉",
        plain_body=(
            "¡Hola {name}! 🚀\n\n"
            "Tu aplicación Congrats está activa y rockeando. 🤘\n\n"
            "Sigue brillando,\nEl equipo de Congrats 🥳"
        ),
        html_body=wrap_html(
            "<p style='font-size:16px;'>¡Hola <strong>{name}</strong>! 🚀</p>"
            "<p style='font-size:16px;margin:24px 0;'>"
            "La prueba de funcionamiento pasó. Tu app está lista para la fiesta. 🎉"
            "</p>"
            "<p style='font-size:16px;margin-top:24px;'>"
            "Sigue brillando.<br><em>El equipo de Congrats 🥳</em>"
            "</p>"
        ),
        required_vars=["name"],
    ),
}