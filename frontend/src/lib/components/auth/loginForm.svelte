<script>
    import {createEventDispatcher} from "svelte";
    import {validateEmail} from "$lib/validators.js";

    const dispatch = createEventDispatcher()
    let email = '';
    let password = '';
    let emailError = '';
    let loginError = '';
    let isLoading = false;
    let apiUrl = import.meta.env.VITE_API_BASE_URL;

    const validateForm = () => {
        emailError = validateEmail(email) ? '' : '유효한 이메일 주소를 입력해주세요.';
        return !emailError
    } ;

    const handleLogin = async () => {
        if (!validateForm()) return;

        isLoading = true;
        loginError = '';

        try {
            const response = await fetch(`${apiUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 401) {
                    loginError = '이메일 또는 비밀번호가 일치하지 않습니다.';
                } else {
                    loginError = errorData.message || '로그인 중 문제가 발생했습니다.';
                }
                return;
            }

            const data = await response.json();
            console.log('로그인 성공:', data);

            // 로그인 성공 시 이벤트 발생
            dispatch('loginSuccess', data);
        } catch (error) {
            console.error('로그인 요청 실패:', error);
            alert('서버 요청 중 문제가 발생했습니다.');
        } finally {
            isLoading = false;
        }
    };
</script>

<div class="flex flex-col items-center justify-center w-screen h-screen bg-gray-200 text-gray-700">
    <h1 class="font-bold text-3xl text-blue-700 drop-shadow-[0_1px_1px_rgba(0,0,0,0.6)]">AI Inspection & Regularization System</h1>

<!--    <form use:form on:submit|preventDefault action="#" method="post" class="flex flex-col bg-white rounded shadow-lg p-12 mt-12">-->
    <form use:form on:submit|preventDefault={handleLogin} class="flex flex-col bg-white rounded shadow-lg p-12 mt-12">
        <label class="font-semibold text-xs" for="email">Email</label>
        <input class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2"
               name="email"
               type="email"
               bind:value={email}
               placeholder="example@sk.com"
               required/>
        <!-- error message -->
        {#if emailError}
            <span class="text-red-500 text-sm">{emailError}</span>
        {/if}
        <!-- -->
        <label class="font-semibold text-xs mt-3" for="password">Password</label>
        <input class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2"
               name="password"
               bind:value={password}
               type="password"
               required />
        <!-- error message -->
        {#if loginError}
            <span class="text-red-500 text-sm">{loginError}</span>
        {/if}
        <!-- -->
        <button class="flex items-center justify-center h-12 px-6 w-64 bg-violet-600 mt-8 rounded-2xl font-semibold text-sm text-violet-100 hover:bg-violet-700"
                disabled={isLoading}>
            {isLoading ? 'Login ...' : 'Login'}
        </button>

        <div class="flex mt-6 justify-center text-xs">
            <a class="text-violet-400 hover:text-violet-500" href="#">Forgot Password</a>
            <span class="mx-2 text-gray-300">/</span>
            <a class="text-violet-400 hover:text-violet-500" href="#">Sign Up</a>
        </div>
    </form>
</div>