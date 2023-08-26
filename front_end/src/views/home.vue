<template>
  <div class="wrap">
    <div class="background"></div>
    <van-popup v-model="show" position="bottom">
      <van-cell-group>
        <van-cell center  value="带雨图像去雨" size="large" @click="derain"/>
        <van-cell center  value="失焦图像去模糊" size="large" @click="defocus_deblur"/>
        <van-cell center  value="运动图像去模糊" size="large" @click="motion_deblur"/>
        <van-cell center  value="噪点图像去噪" size="large" @click="denoise"/>
      </van-cell-group>
    </van-popup>
    <div class="main_buttons">
      
        <label  class="input_buttons">
          <input ref="fileInput" 
                 type="file" 
                 style="display: none;" 
                 accept="image/*"  
                 @change="previewImage">
          <img src="../assets/home_bg/add.png" height="24px">
          导入
        </label>
        <div class="minis">
          <!-- 一键处理按钮 -->
          <div class="mini_buttons" @click="auto_process">
            <div class="img">
              <img src="../assets/buttons/process.png" height="35px">
            </div>
            <div class="font">一键处理</div>
          </div>
          <!-- 选择类型按钮 -->
          <div class="mini_buttons" @click="showPopup" >
            <div class="img">
              <img src="../assets/buttons/choose.png" height="35px">
            </div>
            <div class="font">选择类型</div>
          </div>
          <!-- 判断类型按钮 -->
          <div class="mini_buttons" @click="judge">
            <div class="img">
              <img src="../assets/buttons/decide.png" height="35px">
            </div>
            <div class="font">判断类型</div>
            
          </div>
          <!-- 更多功能正在赶来 -->
          <div class="mini_buttons">
            <div class="img">
              <img src="../assets/buttons/wait.png" height="35px">
            </div>
            <div class="font">更多功能正在赶来</div>
          </div>
        </div>
    </div>
    <div class="tabs">
      <van-tabs>
        <van-tab title="未处理图片">
          <div class="preview_img">
            <van-empty v-if="!imageUrl" description="请上传图片QAQ" />
            <img v-if="imageUrl" :src="imageUrl" width="300px"/>
          </div>
        </van-tab>
        <van-tab title="已处理图片">
          <div class="outcome_img">
            <van-empty v-if="!processed_imgUrl" description="暂无处理后的图片哦~" />
            <img v-if="processed_imgUrl" :src="processed_imgUrl" width="300px"  @click="downloadImage"/>
            <p class="download_text" v-if="processed_imgUrl" >点击图片可下载</p>
          </div>
        </van-tab>
      </van-tabs>

      <van-overlay :show="show_over" @click="show_over = false">
        <div class="wrapper" @click="show_over = false">
          <div class="block">
            <van-loading size="24px" vertical>处理中...</van-loading>
          </div>
        </div>
      </van-overlay>

      <van-overlay :show="show_type_over" @click="show_type_over = false">
        <div class="wrapper_type" @click="show_type_over = false">
          <div class="block_type">
            该图像为：{{this.type}}
          </div>
        </div>
      </van-overlay>

      <van-overlay :show="show_judge_over" @click="show_judge_over = false">
        <div class="wrapper" @click="show_judge_over = false">
          <div class="block">
            <van-loading size="24px" vertical>处理中...</van-loading>
          </div>
        </div>
      </van-overlay>
    </div>
      
  </div>
</template>
<script>
import HttpRequest from '../api/axios.js';
import axios from 'axios';

  export default {
    data() {
      return {
        imageUrl: '',
        out: '',
        type: '',
        processed_imgUrl: '',
        show: false,
        show_over: false,
        show_type_over: false,
        show_judge_over: false,
      }
    },
    mounted(){
    },
    methods:{
      showPopup() {
        this.show = true;
      },
      previewImage() {
        const file = this.$refs.fileInput.files[0]
        const reader = new FileReader()
        console.log(file)
        reader.readAsDataURL(file)
        reader.onload = () => {
          this.imageUrl = reader.result
        }
      },
      auto_process() {
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);
        this.show_over = true
        axios({
          method: 'post',
          url: 'http://192.168.1.165:5000/auto_process',
          data: form,
          responseType: 'arraybuffer'  // 指定响应类型为二进制数据
        }).then(response => {
          // 将接收到的二进制数据转换成Blob对象
          const blob = new Blob([response.data], { type: 'image/jpeg' });
          // 创建一个URL，指向Blob对象的数据
          this.processed_imgUrl = URL.createObjectURL(blob);
          if(this.processed_imgUrl){
            this.show_over = false
          }
        });
      },
      judge() {
        this.show_judge_over = true
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);

        const http = new HttpRequest()
        http.post('http://192.168.1.165:5000/predict', form)
          .then(data => {
            this.type = data.data       
            if (this.type == 'defoucs_blur'){
              this.type = '失焦模糊图像'
            }
            if (this.type == 'motion_blur'){
              this.type = '运动模糊图像'
            }  
            if (this.type == 'rain'){
              this.type = '带雨图像'
            }
            if (this.type == 'Real_Denoising'){
              this.type = '噪点图像'
            }
            this.show_judge_over = false
            this.show_type_over = true
            // 处理成功返回的数据
          })
          .catch(error => {
            console.log(error)
            // 处理失败情况
          })
        },
      derain(){
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);
        this.show_over = true
        this.show = false
        axios({
          method: 'post',
          url: 'http://192.168.1.165:5000/process?data=rain',
          data: form,
          responseType: 'arraybuffer'  // 指定响应类型为二进制数据
        }).then(response => {
          // 将接收到的二进制数据转换成Blob对象
          const blob = new Blob([response.data], { type: 'image/jpeg' });
          // 创建一个URL，指向Blob对象的数据
          this.processed_imgUrl = URL.createObjectURL(blob);
          if(this.processed_imgUrl){
            this.show_over = false
          }
        });
      },
      defocus_deblur(){
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);
        this.show_over = true
        this.show = false
        axios({
          method: 'post',
          url: 'http://192.168.1.165:5000/process?data=defoucs_blur',
          data: form,
          responseType: 'arraybuffer'  // 指定响应类型为二进制数据
        }).then(response => {
          // 将接收到的二进制数据转换成Blob对象
          const blob = new Blob([response.data], { type: 'image/jpeg' });
          // 创建一个URL，指向Blob对象的数据
          this.processed_imgUrl = URL.createObjectURL(blob);
          if(this.processed_imgUrl){
            this.show_over = false
          }
        });
        
      },
      motion_deblur(){
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);
        this.show_over = true
        this.show = false
        axios({
          method: 'post',
          url: 'http://192.168.1.165:5000/process?data=motion_blur',
          data: form,
          responseType: 'arraybuffer'  // 指定响应类型为二进制数据
        }).then(response => {
          // 将接收到的二进制数据转换成Blob对象
          const blob = new Blob([response.data], { type: 'image/jpeg' });
          // 创建一个URL，指向Blob对象的数据
          this.processed_imgUrl = URL.createObjectURL(blob);
          if(this.processed_imgUrl){
            this.show_over = false
          }
        });
        
      },
      denoise(){
        const fileobj = this.$refs.fileInput.files[0]
        var form = new FormData();
        form.append("file", fileobj);
        this.show_over = true
        this.show = false
        axios({
          method: 'post',
          url: 'http://192.168.1.165:5000/process?data=Real_Denoising',
          data: form,
          responseType: 'arraybuffer'  // 指定响应类型为二进制数据
        }).then(response => {
          // 将接收到的二进制数据转换成Blob对象
          const blob = new Blob([response.data], { type: 'image/jpeg' });
          // 创建一个URL，指向Blob对象的数据
          this.processed_imgUrl = URL.createObjectURL(blob);
          if(this.processed_imgUrl){
            this.show_over = false
          }
        });
        
      },
      downloadImage() {
        const link = document.createElement('a')
        link.href = this.processed_imgUrl; 
        link.download = 'image.png' // 设置下载的文件名为图片的名称
        link.click() // 点击链接进行下载
    },
    },
    components:{

    }
  }
</script>
<style lang="stylus" rel="stylesheet/stylus" scoped>
  @import "../common/stylus/mixin.styl";
  .wrap{
    display: flex;
    justify-content: center;
    height: 100vh;
  }
  .background{
    height: 250px; 
    width: 400px;
    background-image: url('../assets/home_bg/sponge.jpg');
    background-size: cover;
    position: relative;
  }
  .main_buttons{
    background-color:white;
    box-shadow: 3px 3px 3px 3px rgba(227, 227, 227, 0.75);
    top: 150px;
    margin: 0 auto;
    padding: 15px;
    height: 160px;
    width: 320px;
    position: absolute;
    /* display: flex; */
  }
  .input_buttons{
      background-color: rgb(0, 0, 0);
      color: white;
      height: 60px;
      width: 320px;
      margin: 0 auto;
      font-family: Arial, sans-serif;
      font-size: 15px;
      display: flex;
      justify-content: center;
      align-items: center;
      /* position: relative; */
    }
    .minis{
      margin-top: 30px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .mini_buttons{
      /* position: absolute; */
      /* top:80px; */
      margin: 0 auto;
    }
    .tabs{
      position: absolute;
      top: 360px;
      width: 350px;
    }
    .img{
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .font{
      margin-top: 10px;
      font-size: 10px;
      font-family:'Times New Roman', Times, serif;
    }
    .preview_img{
      border: 2px;
      margin-top: 10px;
      margin-bottom: 150px;
      padding-bottom: 50px;
      text-align: center;
    }
    .showtext{
      margin: 10px;
      font-family: 'Source Han Sans', sans-serif;
      font-size: 17px;
    }
    .outcome_img{
      border: 2px;
      margin-top: 10px;
      margin-bottom: 150px;
      padding-bottom: 50px;
      text-align: center;
    }
    .wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }
    .block {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 120px;
      height: 120px;
      background-color: #fff;
    }
    .download_text{
      margin-top: 10px;
      color: #a7a5a5;
      font-size: 10px;
    }
    .wrapper_type {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }
    .block_type {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 230px;
      height: 50px;
      background-color: #fff;
      font-family: Arial, sans-serif;
      border-radius: 10%
    }


</style>
