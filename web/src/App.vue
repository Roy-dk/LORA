<template>
  <div> 
    <div v-if="loginShow && finish">
      <div style="height: 60px;text-align: center;display: flex;"></div>

      <div class="custom-card" style="margin-top: 100px;">
        <van-field size="large" v-model="channel" placeholder="例如：01,02...[两位字符]" label="地址" />
        <van-field size="large" v-model="addr" placeholder="例如：23,24...[两位字符]" label="信道" />
        <div style="height: 200px;display: flex;padding:10px">
          <van-button
            hairline
            type="primary"
            size="large"
            round
            style="margin: auto;"
            @click="connect"
          >连接</van-button>
        </div>
      </div>
      <div v-for="c,j in addrList">
        <div>
          <div v-for="a,i in channelList">
            <div class="custom-card" :class="{'processbc':dataList&&dataList[i]&&dataList[i][j]&&dataList[i][j][0]}" style @click="cardClick(addrList[j], channelList[i])">
              <van-field
                size="large"
                v-model="addrList[j]"
                placeholder="例如：01,02...[两位字符]"
                label="地址"
              />
              <van-field
                size="large"
                v-model="channelList[i]"
                placeholder="例如：23,24...[两位字符]"
                label="信道"
              />
              <div style="display: flex;">
                <div style="flex: 1;">
                  <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">温度</div>
                  <div style="margin: 10px;" v-if="dataList&&dataList[i]&&dataList[i][j]&&dataList[i][j][0]">{{ dataList[i][j][0]}}</div>
                </div>
                <div style="flex: 1;">
                  <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">重量</div>
                  <div style="margin: 10px;" v-if="dataList&&dataList[i]&&dataList[i][j]&&(dataList[i][j][1]!=null)">{{ dataList[i][j][1]}}</div>
                </div>
                <div></div>
              </div>
              <div style="margin: 20px;font-size: 16px;font-weight: normal;color: #409EFF;">
                <a>详情</a>
                <van-icon name="arrow" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <van-nav-bar :title="channel + addr  " left-text="返回" left-arrow @click-left="loginShow = true" />
      <div v-if="weight || temperature" class="custom-card" style="display: flex;">
        <div v-if="temperature" style="flex: 1;">
          <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">温度</div>
          <div class="content">{{ temperature }}度</div>
          <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">{{ temperature_date }}</div>
        </div>
        <div v-if="weight" style="flex: 1;">
          <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">重量</div>

          <div class="content">{{ weight }}g</div>
          <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">{{ weight_date }}</div>
        </div>
      </div>
      <div v-if="light" class="custom-card" style="display: flex;">
        <van-cell style="text-align: left;" title="小灯状态">
          <template #right-icon>
            <van-switch @change="lightChange" v-model="lightChecked" />
          </template>
        </van-cell>
      </div>
      <div class="custom-card">
        <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;">最新数据</div>

        <div style="height: 60px;overflow: auto;">
          <div style="font-size: 14px;font-weight: 300;color: #5b5b5b;text-align: left;">{{ log }}</div>
          <div
            style="font-size: 14px;font-weight: 300;color: #5b5b5b;text-align: left;"
          >{{ log_date }}</div>
        </div>
      </div>
      <div class="custom-card">
        <div style="margin-bottom: 4px;color: #00000073;font-size: 14px;"></div>

        <van-field
          size="large"
          v-model="sendText"
          rows="4"
          type="textarea"
          placeholder="内容"
          label="发送数据"
        />
        <div style="height: 100px;display: flex;padding:10px">
          <van-button
            hairline
            type="primary"
            size="large"
            round
            style="margin: auto;"
            @click="sendData"
          >发送</van-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
const temperature = ref("");
const weight = ref("");

const log = ref("");

const temperature_date = ref("");

const weight_date = ref("");

const log_date = ref("");
const light = ref("");
const channel = ref("");
const addr = ref("");
const channelList = ref(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]);
const addrList = ref(["01", "02"]);
const dataList = ref([]);
const light_date = ref("");
const finish = ref(false);
const sendText = ref("");
const lightChecked = ref(true);
const loginShow = ref(true);
import axios from 'axios';
import { Toast } from 'vant';

function getData() {
  axios.get('http://124.223.18.185/api/get_data?id=' + channel.value + addr.value)
    .then(response => {
      console.log(response.data);
      temperature.value = response.data["temperature"];
      weight.value = response.data["weight"];
      log.value = response.data["log"];
      temperature_date.value = response.data["temperature_date"];
      weight_date.value = response.data["weight_date"];
      log_date.value = response.data["log_date"];
      light.value = response.data["light"];
      light_date.value = response.data["light_date"];
      lightChecked.value = response.data["light"] == "1" ? true : false;
    })

}


function getAllData() {
  if (!loginShow.value) {
    return;
  }
  for (let channel_i in channelList.value) {
    let channel_index = channelList.value[channel_i];
    for (let addr_i in addrList.value) {
      let addr_index = addrList.value[addr_i];


console.log(channel_index + addr_index)
      axios.get('http://124.223.18.185/api/get_data?id=' + addr_index+ channel_index )
        .then(response => {
          console.log(response.data);
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1][0] = response.data["temperature"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1][1] = response.data["weight"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].log = response.data["log"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].temperature_date = response.data["temperature_date"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].weight_date = response.data["weight_date"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].log_date = response.data["log_date"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].light = response.data["light"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].light_date = response.data["light_date"];
          dataList.value[parseInt(channel_index)][parseInt(addr_index) - 1].lightChecked = response.data["light"] == "1" ? true : false;

        })
    }
  }

}

function cardClick(v1, v2) {
  channel.value = v1;
  addr.value = v2;
  connect();
}
function get2Tem(v1, v2) {
  console.log(dataList.value, v1, v2);
  console.log(dataList.value[(v1)][(v2)]);
  if (dataList.value[(v1)][(v2)])
    return dataList.value[(v1)][(v2)]["temperature"];
  return "";
}
function get2Wei(v1, v2) {
  console.log(dataList.value, v1, v2);
  if (dataList.value[(v1)][(v2)])
    return dataList.value[(v1)][(v2)]["weight"];
  return "";
}

function lightChange(value) {
  let l = "0";
  if (value) {
    l = "1";
  }
  else {
    l = "0";

  }
  axios.get('http://124.223.18.185/api/send_data?id=' + channel.value + addr.value + "&data=" + l)
    .then(response => {
      if (response.data.code == 0) {
        Toast("发送成功！");
      }
    })
}

function sendData() {
  axios.get('http://124.223.18.185/api/send_data?id=' + channel.value + addr.value + "&data=" + sendText.value)
    .then(response => {
      if (response.data.code == 0) {
        Toast("发送成功！");
      }
    })
}
onMounted(() => {

  for (let channel_i in channelList.value) {
    let channel_index = channelList.value[channel_i];
    dataList.value[channel_i] = [];
    for (let addr_i in addrList.value) {
      let addr_index = addrList.value[addr_i];
      console.log(addr_index);
      dataList.value[channel_i][addr_i] = [];


    }
  }
  finish.value = true;
  var t2 = window.setInterval(getAllData, 2000)
})

function connect() {
  if (channel.value.length != 2 || addr.value.length != 2) {
    Toast("格式错误，重新输入！");
    return;
  }
  loginShow.value = false;
  getData();
  var t2 = window.setInterval(getData, 500)
}
</script>

<style>
.button:active {
  background-color: #fff;
}
.custom-card {
  margin: 10px;
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0px 20px 27px rgb(0 0 0 / 5%);
  transition: all 0.3s;
}
.content {
  color: #000000d9;
  line-height: 33px;
  font-size: 24px;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto,
    Helvetica Neue, Arial, Noto Sans, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", Segoe UI Symbol, "Noto Color Emoji";
}
  .processbc{
    background-image: linear-gradient(125deg,#E4FFCD,#6dd4fa7c,#b0b65b77,#E4FFCD);
    background-size: 400%;
    animation: bganimation 5s infinite;
  }
  .van-cell {
    background-color: rgba(255, 255, 255, 0)!important;

  }
</style>
