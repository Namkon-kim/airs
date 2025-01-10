// 이메일 유효성 검사
export function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 비밀번호 유효성 검사
export function validatePassword(password) {
    const passwordRegex = /^(?=.*[!@#$%^&*])(?=.{8,})/;
    return passwordRegex.test(password);
}
