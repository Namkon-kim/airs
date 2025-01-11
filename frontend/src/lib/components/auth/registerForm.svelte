<script>
    import { validateEmail, validatePassword } from '$lib/validators';

    let email = '';
    let password = '';
    let confirmPassword = '';
    let emailError = '';
    let passwordError = '';
    let confirmPasswordError = '';
    let isLoading = false;

    const validateForm = () => {
        emailError = validateEmail(email) ? '' : '유효한 이메일 주소를 입력해주세요.';
        passwordError = validatePassword(password)
            ? ''
            : '비밀번호는 8자리 이상이고 특수문자를 포함해야 합니다.';
        confirmPasswordError =
            password === confirmPassword ? '' : '비밀번호가 일치하지 않습니다.';
        return !emailError && !passwordError && !confirmPasswordError;
    };

    const handleRegister = async () => {
        if (!validateForm()) return;

        isLoading = true;

        try {
            // API 호출 (POST 요청)
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`회원가입 실패: ${errorData.message}`);
                return;
            }

            alert('회원가입 성공! 로그인 해주세요.');
        } catch (error) {
            console.error('회원가입 요청 실패:', error);
            alert('서버 요청 중 문제가 발생했습니다.');
        } finally {
            isLoading = false;
        }
    };
</script>

<div class="flex flex-col items-center justify-center w-screen h-screen bg-gray-200 text-gray-700">
    <h1 class="font-bold text-3xl text-blue-700 drop-shadow-[0_1px_1px_rgba(0,0,0,0.6)]">
        AI Inspection & Regularization System
    </h1>

    <form
            use:form
            on:submit|preventDefault={handleRegister}
            class="flex flex-col bg-white rounded shadow-lg p-12 mt-12"
    >
        <!-- Email -->
        <label class="font-semibold text-xs" for="email">Email</label>
        <input
                class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2"
                name="email"
                type="email"
                bind:value={email}
                placeholder="example@sk.com"
                required
        />
        {#if emailError}
            <span class="text-red-500 text-sm">{emailError}</span>
        {/if}

        <!-- Password -->
        <label class="font-semibold text-xs mt-3" for="password">Password</label>
        <input
                class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2"
                name="password"
                type="password"
                bind:value={password}
                placeholder="비밀번호를 입력하세요"
                required
        />
        {#if passwordError}
            <span class="text-red-500 text-sm">{passwordError}</span>
        {/if}

        <!-- Confirm Password -->
        <label class="font-semibold text-xs mt-3" for="confirmPassword">Confirm Password</label>
        <input
                class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2"
                name="confirmPassword"
                type="password"
                bind:value={confirmPassword}
                placeholder="비밀번호를 다시 입력하세요"
                required
        />
        {#if confirmPasswordError}
            <span class="text-red-500 text-sm">{confirmPasswordError}</span>
        {/if}

        <!-- Submit Button -->
        <button
                class="flex items-center justify-center h-12 px-6 w-64 bg-violet-600 mt-8 rounded-2xl font-semibold text-sm text-violet-100 hover:bg-violet-700"
                disabled={isLoading}
        >
            {isLoading ? 'Registering ...' : 'Register'}
        </button>

        <div class="flex mt-6 justify-center text-xs">
            <a class="text-violet-400 hover:text-violet-500" href="#">Already have an account? Login</a>
        </div>
    </form>
</div>
