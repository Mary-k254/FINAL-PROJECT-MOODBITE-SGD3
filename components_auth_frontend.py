from __future__ import annotations  # ← ADD THIS
import flet as ft
import httpx

class AuthManager:
    def __init__(self, page):
        self.page = page
        self.token = None
        self.base_url = "http://localhost:8000/api/v1"
    
    def get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
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
                    self.page.client_storage.set("auth_token", self.token)
                    return True, "Login successful"
                else:
                    return False, "Invalid credentials"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    async def register(self, email, password, full_name):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/users/register",
                    json={
                        "email": email, 
                        "password": password, 
                        "full_name": full_name,
                        "consent_given": True
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                    self.page.client_storage.set("auth_token", self.token)
                    return True, "Registration successful"
                else:
                    error_data = response.json()
                    return False, error_data.get("detail", "Registration failed")
        except Exception as e:
            return False, f"Connection error: {str(e)}"

def create_login_page(page, auth_manager):
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    result_text = ft.Text("", color="red")
    
    async def handle_login(e):
        success, message = await auth_manager.login(email_field.value, password_field.value)
        if success:
            result_text.value = "Login successful!"
            result_text.color = "green"
            await page.go_async("/dashboard")
        else:
            result_text.value = message
            result_text.color = "red"
        await page.update_async()
    
    async def go_to_register(e):
        await page.go_async("/register")
    
    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("MoodBite - Login"), bgcolor="blue"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Login to MoodBite", size=24, weight="bold"),
                        email_field,
                        password_field,
                        ft.ElevatedButton("Login", on_click=handle_login),
                        ft.TextButton("Don't have an account? Register here", on_click=go_to_register),
                        result_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )