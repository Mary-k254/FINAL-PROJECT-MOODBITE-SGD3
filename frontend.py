import flet as ft
import httpx

class AuthManager:
    def __init__(self, page):
        self.page = page
        self.token = None
        self.base_url = "http://localhost:8000/api/v1"
    
    async def login(self, email, password):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/users/login",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                    return True, "Login successful"
                else:
                    return False, "Invalid credentials"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

def main(page: ft.Page):
    page.title = "MoodBite"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    auth_manager = AuthManager(page)
    
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    result_text = ft.Text("", color="red")
    
    async def handle_login(e):
        success, message = await auth_manager.login(email_field.value, password_field.value)
        if success:
            result_text.value = "Login successful!"
            result_text.color = "green"
        else:
            result_text.value = message
            result_text.color = "red"
        page.update()
    
    page.add(
        ft.Column([
            ft.Text("MoodBite Login", size=20),
            email_field,
            password_field,
            ft.ElevatedButton("Login", on_click=handle_login),
            result_text
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

# Run in web browser instead of desktop
ft.app(target=main, view=ft.AppView.WEB_BROWSER)