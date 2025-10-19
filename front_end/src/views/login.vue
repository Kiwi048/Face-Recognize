<template>
  <div class="login-container">
    <div class="form-box">
      <h2>{{ isLogin ? '用户登录' : '用户注册' }}</h2>
      <form @submit.prevent="isLogin ? handleLogin() : handleRegister()">
        
        <!-- 登录表单 -->
        <div v-if="isLogin">
          <input v-model="form.account" placeholder="账号" required />
          <input v-model="form.password" type="password" placeholder="密码" required />
        </div>

        <!-- 登录表单 -->
        <div v-else>
<<<<<<< HEAD
          <input v-model="registerForm.name" placeholder="姓名" required />
          <input v-model="registerForm.account" placeholder="账号" required />
          <input v-model="registerForm.password" type="password" placeholder="密码" required />
          
          <input type="hidden" v-model="registerForm.role" />

          <div class="camera-box">
            <video ref="video" autoplay playsinline></video>
            <button type="button" @click="capturePhoto">拍照录入</button>
          </div>

          <div v-if="photoData">
            <img :src="photoData" alt="captured face" style="max-width:100px;" />
          </div>
        </div>

        <button type="submit">{{ isLogin ? '登录' : '注册' }}</button>
=======
          <input v-model="registerForm.account" placeholder="工号（五位小写英文+三位数字）" required />
          <input v-model="registerForm.password" type="password" placeholder="密码" required />
        </div>
        <button type="submit" class="submit-button">{{ isLogin ? '登录' : '注册' }}</button>
>>>>>>> upstream/main
      </form>
      <p @click="toggleForm" class="toggle-link">
        {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
      </p>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
<<<<<<< HEAD
  return {
    isLogin: true,
    form: { account: '', password: '' },
    registerForm: {
  name: '',
  account: '',
  password: '',
  role: '员工',   // 默认员工
  face_photo: ''  // 用来保存人脸照片(base64)
},

    message: '',
    photoData: ''
  }
},
methods: {
   toggleForm() {
    this.isLogin = !this.isLogin;
    this.message = '';
    if (!this.isLogin) {
      this.$nextTick(() => {
        this.mountedCamera();
      });
    }
  },
  
async handleLogin() {
        try {
            const res = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.form)
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                this.message = '登录成功，正在跳转...';
                
                // 暂时用 alert 模拟跳转
                // 后续其他部分完成后，可以改成 this.$router.push('/admin') 或 this.$router.push('/home')
                setTimeout(() => {
                    if (data.user.role === '管理员') {
                        alert('管理员登录成功！准备跳转到管理员页面...');
                    } else {
                        alert('员工登录成功！准备跳转到员工页面...');
                    }
                    // this.$router.push('/some-page'); // 实际跳转
                }, 1000);

            } else {
                this.message = data.message || '登录失败';
            }
        } catch (err) {
            this.message = '网络错误，请检查后端服务是否已启动';
        }
    },
  async mountedCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      this.$refs.video.srcObject = stream;
    } catch (err) {
      console.error("摄像头调用失败", err);
      this.message = "无法访问摄像头";
=======
    return {
      isLogin: true,
      form: {
        account: '',
        password: ''
      },
      registerForm: {
        name: '',
        account: '',
        password: '',
        role: '员工'
      },
      message: ''
    }
  },
  methods: {
    toggleForm() {
          if (this.isLogin) {
              this.$router.push('/register');
        } else {
            this.$router.push('/');
        }
    },
    async handleLogin() {
      try {
        const res = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form)
        });
        const data = await res.json();
        if (res.ok) {
          this.message = '登录成功';
          
          // 保存token和用户信息
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('user_info', JSON.stringify(data.user));
          
          // 根据用户角色跳转页面
          if (data.user.role === '管理员') {
            this.$router.push('/admin');
          } else {
            // 普通用户页面（暂时跳转到管理员页面，您可以后续创建普通用户页面）
            this.$router.push('/admin');
          }
        } else {
          this.message = data.message || '登录失败';
        }
      } catch (err) {
        this.message = '网络错误';
      }
    },
    async handleRegister() {
      try {
        const res = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.registerForm)
        });
        const data = await res.json();
        if (res.ok) {
          this.message = '注册成功，下一步将跳转录入人脸信息...';
          
          await new Promise(resolve => setTimeout(resolve, 500));
          // 通过路由参数传递用户信息到人脸录入页面
          console.log("注册返回的用户信息:", JSON.stringify(data.user));
          this.$router.push({
            path: '/face-register',
            query: {
              userInfo: JSON.stringify(data.user),
              register: 'true'
            }
          });
          this.isLogin = true;
        } else {
          // 显示后端返回的错误信息，包括账号已存在的提示
          this.message = data.message || '注册失败';
        }
      } catch (err) {
        this.message = '网络错误';
      }
>>>>>>> upstream/main
    }
  },
capturePhoto() {
  const canvas = document.createElement('canvas');
  const video = this.$refs.video;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  this.photoData = canvas.toDataURL('image/jpeg'); // base64
  this.registerForm.face_photo = this.photoData;
},
 async handleRegister() {
        // 注册成功后，自动切换到登录页，并清空消息
        if (!this.registerForm.face_photo) {
            this.message = '请先拍照录入人脸';
            return;
        }
        try {
            const res = await fetch('http://localhost:5000/register', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.registerForm)
            });
            const data = await res.json();
            if (res.ok) {
                this.message = '注册成功！请使用新账号登录。';
                this.isLogin = true; // 切换回登录界面
                // 清空注册表单
                this.registerForm = { name: '', account: '', password: '', role: '员工', face_photo: '' };
                this.photoData = '';
            } else {
                this.message = data.message || '注册失败';
            }
        } catch (err) {
            this.message = '网络错误，请检查后端服务是否已启动';
        }
}},
mounted() {
  if (!this.isLogin) {
    this.mountedCamera();
  }
}
,
  watch: {
    '$route'(to) {
      this.isLogin = to.name !== 'RegisterPage';
      this.message = '';
    }
    }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f6fa;
}
.form-box {
  background: #fff;
  padding: 32px 40px;
  border-radius: 8px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  min-width: 320px;
}
.form-box h2 {
  text-align: center;
  margin-bottom: 24px;
}
.form-box input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
/* 通用按钮样式 */
.form-box button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* 提交按钮样式 */
.form-box .submit-button {
  width: 100%;
  background: #3498db;
  color: #fff;
}

.form-box .submit-button:hover {
  background: #2980b9;
}


.toggle-link {
  color: #3498db;
  text-align: center;
  cursor: pointer;
  margin-top: 12px;
}
.message {
  text-align: center;
  color: #e74c3c;
  margin-top: 10px;
}
</style>