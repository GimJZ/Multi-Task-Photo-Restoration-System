<template>
    <div class="wrap">
      <div class="content">
        <img src="../assets/title.png" width="100px"/>
        <!-- <p>图像修复</p>
        <p>我们是认真的</p> -->
        <van-field v-model="text" label="账号" />
        <van-field v-model="password" type="password" label="密码" />
        <button @click.prevent="login">登录</button>
      </div>
    </div>
  </template>
  
  <script>
    export default {
      data() {
        return {
          text: '',
          password: '',
        }
      },
      mounted(){
      },
      methods:{
        login() {
            // 实现登录逻辑
            this.$router.push('/home');
        }
      },
      components:{
  
      }
    }
  </script>
  <style lang="stylus" rel="stylesheet/stylus" scoped>
    .wrap{
        /* background-color: #cccccc;  */
        height: 100vh;     
    }
    .content{  
        display: flex;
        flex-direction: column;
        /* justify-content: center; */
        align-items: center;
        padding: 20px;
        border-radius: 5px;

    }
    .login {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    img{
      margin-top: 120px;
      margin-bottom: 40px;
    }
    p{
      margin-bottom: 100px;
      font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif
    }
    button {
      background-color: #000000;
      color: white;
      margin-top: 20px;
      padding: 10px 20px;
      border-radius: 5px;
      height: 45px;
      width: 300px;
      cursor: pointer;
    }
  
  </style>
  