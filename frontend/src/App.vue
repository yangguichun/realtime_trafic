<template>
  <div id="app">
    <el-container>
      <el-header>充电站使用率分析</el-header>
      <el-container>
        <el-aside width="15%">
          <p class='station-title'>电站列表</p>
          <el-tree
            :data="stationList"
            :props="treeProps"
            ref='stationTree'
            node-key="id"
            default-expand-all
            show-checkbox
            @check="handleStationCheckChange"
          ></el-tree>
        </el-aside>
        <el-main>
          <el-row>
            <el-col :span="8">
              <el-radio v-model="stationDataType" @change="handleDataTypeChange" label="percent">使用率</el-radio>
              <el-radio
                v-model="stationDataType"
                @change="handleDataTypeChange"
                label="pilecount"
              >使用的桩个数</el-radio>
            </el-col>
            <el-col :span="16">
              <div class="block">
                <el-button @click="previous" type="primary">前一天</el-button>
                <el-button @click="current" type="primary">今天</el-button>
                <el-button @click="next" type="primary">后一天</el-button>

                <span class="demonstration"></span>
                <el-date-picker
                  v-model="currentDate"
                  align="right"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions1"
                  @change="selectedDateChange"
                ></el-date-picker>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <div class="mychart" ref="myEchart"></div>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import echarts from "echarts";
export default {
  data() {
    return {
      chart: null,
      chartOption: null,
      currentDate: new Date(),
      stationList: [],
      treeProps:{
        label: 'name',
        children: 'children'
      },
      stationDataType: "percent",
      selStationIdList: [4],
      pickerOptions1: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            }
          },
          {
            text: "昨天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            }
          },
          {
            text: "一周前",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            }
          }
        ]
      }
    };
  },
  mounted() {
    this.initStationList();
    this.$refs['stationTree'].setCheckedKeys(this.selStationIdList)
    this.initChart();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.myEchart);
      this.current();
    },
    initStationList() {
      this.$http.get("/getstationtree").then(r => {
        let data = r.body;
        this.stationList = data.stationList;
      });
    },
    handleStationCheckChange(data, checkedInfo) {
      this.selStationIdList = checkedInfo.checkedKeys
      this.queryData();
    },
    handleDataTypeChange() {
      this.queryData();
    },
    previous() {
      let tempDate = new Date(this.currentDate);
      tempDate.setTime(tempDate.getTime() - 3600 * 1000 * 24);
      this.currentDate = tempDate;
      this.queryData();
    },
    next() {
      let tempDate = new Date(this.currentDate);
      tempDate.setTime(tempDate.getTime() + 3600 * 1000 * 24);
      this.currentDate = tempDate;
      this.queryData();
    },
    current() {
      this.currentDate = new Date(this.getDateString(new Date));
      this.queryData();
    },
    selectedDateChange(val){
      //如果不处理下，则传给后端之后就是减了8小时
      this.currentDate = new Date(this.getDateString(val))
      this.queryData();
    },
    getDateString(date) {
      var seperator1 = "-";
      var year = date.getFullYear();
      var month = date.getMonth() + 1;
      var strDate = date.getDate();
      if (month >= 1 && month <= 9) {
        month = "0" + month;
      }
      if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
      }
      var currentdate = year + seperator1 + month + seperator1 + strDate;
      return currentdate;
    },
    getOriginalOption() {
      var colors = ["#5793f3", "#d14a61", "#675bba"];
      let option = {
        color: colors,

        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross"
          }
        },
        legend: {
          data: []
        },
        grid: {
          top: 70,
          bottom: 50
        },
        xAxis: [
          {
            type: "category",
            axisTick: {
              alignWithLabel: true
            },
            axisLine: {
              onZero: false,
              lineStyle: {
                color: colors[1]
              }
            },
            data: null
          }
        ],
        yAxis: [
          {
            type: "value"
          }
        ],
        series: null
      };
      return option;
    },

    queryData() {
      let endTime = new Date(this.currentDate);
      endTime.setTime(endTime.getTime() + 3600 * 1000 * 24);

      let queryParam = {
        ids: this.selStationIdList,
        beginTime: this.currentDate,
        endTime: endTime
      };
      let url = "/querystatus_percent";
      if (this.stationDataType != "percent") {
        url = "/querystatus_num";
      }

      this.$http.post(url, queryParam).then(r => {
        let data = r.body;
        let stationList = data.stationList;
        let stationNameList = [];

        let dateList = null;
        let seriesList = [];
        for (let key in stationList) {
          stationNameList.push(stationList[key].name);

          if (dateList == null) {
            dateList = stationList[key].value.map(item => {
              return item[0];
            });
          }

          let valueList = stationList[key].value.map(function(item) {
            return item[1];
          });

          let oneSerie = {
            name: stationList[key].name,
            type: "line",
            smooth: true,
            data: valueList
          };
          seriesList.push(oneSerie);
        }

        if (this.chartOption == null) {
          this.chartOption = this.getOriginalOption();
        }
        this.chartOption.legend.data = stationNameList;
        this.chartOption.xAxis[0].data = dateList;
        this.chartOption.series = seriesList;
        this.chart.setOption(this.chartOption, true);
      });
    }
  }
};
</script>

<style>
.station-title{
  text-align: left
}
.mychart {
  margin-top: 20px;
  width: 100%;
  height: 500px;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  width: 1800px;
  height: 900px;
  /* width: 100%;
  height: 100%; */
}
</style>
