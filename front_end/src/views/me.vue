<template>
  <div class="wrap">
    <div class="content">
      <div class="imge">
        <img src="../assets/title.png" width="80px"/>
      </div>
      <van-cell-group inset>
        <van-cell title="用户名" value="周俊哲" />
        <van-cell title="账号" value="153XXXXXX23"/>
        <van-cell title="学校" value="杭州电子科技大学"/>
        <van-cell title="学院" value="计算机科学与技术"/>
        <van-cell title="身份" value="学生开发者"/>
        <van-cell title="注册日期" value="2023-5-2"/>
        <van-cell title="其它" value="此软件为本人毕业设计成果，如需引用或使用，需经本人同意"/>
      </van-cell-group>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
      }
    },
    mounted(){
    },
    methods:{
    },
    components:{
    }
  }
</script>
<style lang="stylus" rel="stylesheet/stylus" scoped>
  .wrap{
    height: 100vh;
  }
  .content{
    width: 100%;
  }
  .imge{
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
  img{
    margin-top: 20px;
    margin-left: 15px;
  }

</style>
