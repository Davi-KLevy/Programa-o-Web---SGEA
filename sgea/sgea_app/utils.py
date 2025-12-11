import base64
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def enviar_email_confirmacao(usuario, request):
    """
    Gera e 'envia' (console backend) o e-mail de verificação,
    com a logo inline em Base64 e link de ativação.
    """

    # Token seguro
    token = default_token_generator.make_token(usuario)

    # URL de ativação
    link_ativacao = request.build_absolute_uri(
        reverse("ativar_conta", kwargs={"uid": usuario.id, "token": token})
    )

    # Logo embutida em base 64
    caminho_logo = "/mnt/data/sgea - logo.jpg"
    with open(caminho_logo, "rb") as img:
        logo_base64 = base64.b64encode(img.read()).decode("utf-8")

    # Html do e-mail
    html = f"""
    <div style="font-family: Arial; padding: 20px;">
        <img src="data:image/jpeg;base64,{logo_base64}"
             alt="Logo SGEA"
             style="width: 160px; margin-bottom: 20px; border-radius: 8px;" />

        <h2>Bem-vindo(a) ao SGEA!</h2>

        <p>Olá <strong>{usuario.nome}</strong>,</p>

        <p>Seu cadastro foi realizado com sucesso!</p>

        <p>Para ativar sua conta e acessar o sistema, clique no link abaixo:</p>

        <p>
            <a href="{link_ativacao}"
               style="background-color:#2b74ff; color:white; padding:10px 18px; 
                      text-decoration:none; border-radius:6px;">
                Ativar minha conta
            </a>
        </p>

        <p>Ou copie e cole no navegador:</p>
        <p>{link_ativacao}</p>

        <br>
        <p>Atenciosamente,<br>Equipe SGEA</p>
    </div>
    """

    # Assunto e envio (console backend / SMTP)
    email = EmailMultiAlternatives(
        subject="Confirmação de Cadastro - SGEA",
        body="Seu cliente de e-mail não suporta HTML.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[usuario.login],  # login é o e-mail do usuário
    )
    email.attach_alternative(html, "text/html")
    email.send()
