<!DOCTYPE html>
<html>
<body>
    <h2>Orbit SNS 회원가입</h2>
    <form id="signupForm">
        <input type="text" id="name" placeholder="이름" required><br>
        <input type="email" id="email" placeholder="이메일" required><br>
        <input type="password" id="password" placeholder="비밀번호" required><br>
        <button type="submit">가입하기</button>
    </form>

    <script>
        document.getElementById('signupForm').onsubmit = async (e) => {
            e.preventDefault();
            const response = await fetch('/signup/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value
                })
            });
            const result = await response.json();
            alert(result.message || "에러 발생!");
        };
    </script>
</body>
</html>