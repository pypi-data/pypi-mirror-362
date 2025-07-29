import firebase_admin
from firebase_admin import credentials, messaging


class FirebaseService:
    def __init__(self, cred_path: str):
        # Tải khóa tài khoản dịch vụ từ tệp JSON và khởi tạo ứng dụng Firebase
        # Admin
        cred = credentials.Certificate(cred_path)
        print(cred._g_credential._signer.__dict__, cred_path)
        firebase_admin.initialize_app(cred)

    def send_notification(self, token: str, title: str, body: str) -> str:
        # Tạo thông báo
        # print(f"body: {body}")
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
            ),
            token=token,
            data={
                "title": title,
                "body": body,
            },
        )
        # message = messaging.Message(
        #     data={  # Chỉ gửi payload dữ liệu mà không có thông báo
        #             "title": title,
        #             "body": body,
        #     },
        #     token=token
        # )
        # Gửi thông báo và trả về ID của thông báo
        response = messaging.send(message)
        return response

    def send_notification_to_tokens(
        self, tokens: list[str], title: str, body: str
    ) -> str:
        # Tạo thông báo
        # messages = [
        #     messaging.Message(
        #         notification=messaging.Notification(
        #             title=title,
        #             body=body,
        #         ),
        #         token=token
        #     )
        #     for token in tokens
        # ]
        messages = [
            messaging.Message(
                data={  # Chỉ gửi payload dữ liệu mà không có thông báo
                    "title": title,
                    "body": body,
                },
                token=token,
            )
            for token in tokens
        ]
        response = messaging.send_all(messages)
        print(response.__dict__["_responses"][0].__dict__)
        print(title, type(body))
        return {
            "success_count": response.success_count,
            "failure_count": response.failure_count,
        }
