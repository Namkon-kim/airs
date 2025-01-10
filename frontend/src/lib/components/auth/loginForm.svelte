<div class="flex flex-col items-center justify-center w-screen h-screen bg-gray-200 text-gray-700">
    <h1 class="font-bold text-3xl text-blue-700 drop-shadow-[0_1px_1px_rgba(0,0,0,0.6)]">AI Inspection & Regularization System</h1>

    <form use:form on:submit|preventDefault action="#" method="post" class="flex flex-col bg-white rounded shadow-lg p-12 mt-12">
        <label class="font-semibold text-xs" for="email">Email</label>
        <input class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2" name="email" type="email" />
        <!-- error message -->
        <span class="text-red-500 text-sm"></span>
        <!-- -->
        <label class="font-semibold text-xs mt-3" for="password">Password</label>
        <input class="flex items-center h-12 px-4 w-64 bg-gray-200 mt-2 rounded focus:outline-none focus:ring-2" name="password" type="password" />
        <!-- error message -->
        <span class="text-red-500 text-sm"></span>
        <!-- -->
        <button class="flex items-center justify-center h-12 px-6 w-64 bg-violet-600 mt-8 rounded-2xl font-semibold text-sm text-violet-100 hover:bg-violet-700">Login</button>

        <div class="flex mt-6 justify-center text-xs">
            <a class="text-violet-400 hover:text-violet-500" href="#">Forgot Password</a>
            <span class="mx-2 text-gray-300">/</span>
            <a class="text-violet-400 hover:text-violet-500" href="#">Sign Up</a>
        </div>
    </form>
</div>