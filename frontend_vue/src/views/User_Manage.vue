<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>사용자 관리</v-toolbar-title>

          <v-spacer></v-spacer>

          <template v-slot:extension>
            <v-tabs
                v-model="selected_tab_item"
                align-with-title
                slider-size="6"
            >
              <v-tabs-slider color="yellow"></v-tabs-slider>

              <v-tab
                  v-for="item in type_tab_items"
                  :key="item"
                  @change="change_tab_item(item)"
              >
                {{ item }}
              </v-tab>
            </v-tabs>
          </template>
        </v-toolbar>
        <v-tabs-items v-model="selected_tab_item">
          <v-tab-item
              v-for="(type_item) in type_tab_items"
              :key="type_item">
            <v-card flat>
              <br>
              <v-toolbar rounded dense class="elevation-1">
                <template v-if="type_item === type_tab_items[0]">
                  <v-col cols="10">
                    <v-text-field outlined dense hide-details
                                  placeholder="사용자 검색"
                                  append-icon="mdi-magnify"
                                  v-model="users.search_text"
                                  @keydown.enter="getUsers(type_item)"
                                  class="m-right"
                    />
                  </v-col>
                  <v-col cols="2">
                    <v-btn depressed dark big
                           color="light-blue darken-2"
                           @click="getUsers(type_item)">
                      <v-icon small>mdi-magnify</v-icon>
                      <div class="ml-1">조회</div>
                    </v-btn>
                  </v-col>
                </template>

              </v-toolbar>
              <v-data-table
                v-model="users.selected"
                :headers="getHeaders(type_item)"
                :items="users.data"
                :loading="users.loading"
                :options.sync="users.options"
                :server-items-length="users.total"
                :items-per-page="5"
                :show-select="type_item ==type_tab_items[0]"
                :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
                class="elevation-1 mt-4 clickable-row"
                @click:row="popupDialogShow"
                @input="onSelectedChnage"
              >
                <template v-slot:[`item.id`]="{item}">
                  {{item._index}}
                </template>
                <template v-slot:[`item.user_type`]="{item}">
                  {{getUserTypeName(item.user_type)}}
                </template>
                <template v-slot:[`item.created_date`]="{item}">
                  {{ item.created_date | moment('YYYY-MM-DD HH:mm:ss')}}
                </template>
                <template v-slot:[`item.last_logon_time`]="{item}">
                  {{ item.last_logon_time | moment('YYYY-MM-DD HH:mm:ss')}}
                </template>
                <template v-slot:[`item.created`]="{item}">
                  {{ item.created | moment('YYYY-MM-DD HH:mm:ss')}}
                </template>
              </v-data-table>
              
            </v-card>
          </v-tab-item>

          <v-dialog v-model="popup.user.show" persistent max-width="1000px" max-height="500px">
            <div class="user-info-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="user-info-close" @click="popup.user.show=false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <user-info :userinfo="popup.user.data" @refresh_list="getUsers(type_tab_items[selected_tab_item]);popup.user.show=false" :call_type="{myinfo:false,regist:false,userlist_add:false,userlist_modify:true}" :key="popup.user.data.user_id"/>
            </div>
          </v-dialog>
        </v-tabs-items>
      </div>
    </template>
  </main-layout>
</template>

<script>
import UserInfo from '@/components/UserInfo'
import moment from "moment";
export default {
  props: {
    fstatus: { type: [Number, String], default: 0 }
  },
  components: {UserInfo},
  methods: {
    async getUsers (type_item) {
      console.log("type_item :" + type_item)
      this.users.loading = true;
      const { page, itemsPerPage ,sortBy, sortDesc  } = this.users.options;
      let order_by = []
      let filters_or = [];
      let filters_and = [];
      var api_name = 'users'
      // 정렬 선택이 있을 경우
      if (sortBy.length) {
        for (let i=0; i<sortBy.length; i++) {
          order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
        }
      }
      // 정렬 선택이 없을 경우 id를 기본으로 정렬
      else order_by.push({field: 'id', direction: 'desc'})
      filters_or.push({"name": "user_id", "op": "like", "val": "%"+this.users.search_text+"%"});

      if(this.users.search_text.length > 0) {
        filters_or.push({"name": "user_name", "op": "like", "val": "%" + this.users.search_text + "%"});
      }

      try {
        let q = JSON.stringify({
          filters: [{or:filters_or},{and:filters_and}],
          order_by
        })
        let params = {
          q: q,
          results_per_page: itemsPerPage,
          page: page,
        }

        let { data } = await this.$http.get(api_name, { params })
        this.users.total = data.num_results;
        this.users.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          if(type_item != this.type_tab_items[2]) {
            v.user_status_0 = (v.user_status == 1) ? false : true;
            v.user_status_1 = (v.user_status == 0) ? false : true;
            v.enable = false;
          }else{
            if (v.type == 0) v.type = "로그인";
            else v.type = "로그아웃";
          }
          return v;

        })
      } 
      catch (err) {
        console.error(err);
      } 
      finally {
        this.users.loading = false;
      }
    },
    popupDialogShow(item) {
      if(this.selected_tab_item != 0)
        return
      this.popup.user.data = item
      this.popup.user.show = true;

    },
    getMemberType(type){
      return this.member_type[type-1]
    },
    change_tab_item(item){
      this.users.options.page=1
      this.users.search_text = ""
      this.getUsers(item);
    },
    getHeaders(type_item){
      if(type_item == this.type_tab_items[0]){
        return this.users.headers_user
      }
      return this.users.headers_history
    },
    getAreaCodeName(type_item,area_code){
      if(type_item == this.type_tab_items[1]){
        return area_code
      }

      for(var i=0;i<this.member_area_type.length;i++){
        if(this.member_area_type[i].value == area_code)
          return this.member_area_type[i].text
      }
      return '-'
    },
    getUserTypeName(user_type){
      for(var i=0;i<this.member_user_type.length;i++){
        if(this.member_user_type[i].code == user_type)
          return this.member_user_type[i].name
      }
      return ''
    },
    onUserTypeChage(index){
      this.member_user_type.forEach(v => v.check = false)
      this.member_user_type[index].check = true
    },
    onChangeCheckStauts1(item){
      this.users.data[this.users.data.indexOf(item)].user_status_1 = (item.user_status_0 == true)? false:true
      this.users.data[this.users.data.indexOf(item)].user_status = (item.user_status_0 == true)? 0:1
      this.users.selected.forEach( function(v) {
        if(v == item) {
          v.user_status = item.user_status;
        }
      })
    },
    onChangeCheckStauts2(item){
      this.users.data[this.users.data.indexOf(item)].user_status_0 = (item.user_status_1 == true)? false:true
      this.users.data[this.users.data.indexOf(item)].user_status = (item.user_status_1 == true)? 1:0
      this.users.selected.forEach( function(v) {
        if(v == item) {
          v.user_status = item.user_status;
        }
      })
    },
    onSelectedChnage(){
      this.users.data.forEach(v=>v.enable=false)
      this.users.selected.forEach(v=>v.enable=true)
    },
    async applyUserStatus(){

      for(var i=0;i<this.users.selected.length;i++){
        for(var j=0;j<this.users.data.length;j++){
          if(this.users.selected[i].user_id == this.users.data[j].user_id){
            let params = {}
            params.user_id = this.users.data[j].user_id;
            params.user_status = this.users.data[j].user_status
            await this.$http.patch(`users/${this.users.data[j].id}`, params)
          }
        }
      }
      this.getUsers(this.type_tab_items[this.selected_tab_item])
      this.users.selected = []
    },
    getMemberName(name){
      if(name == undefined || name == ''){
        return '-'
      }
      return name
    }
  },
  mounted() {
    this.users.search.selected_user_type = this.member_user_type_m[0].code
    this.users.search.selected_user_status = this.member_user_status_m[0].value
    this.users.search.selected_area_type = this.member_area_type_m[0].value
    this.users.search.selected_user_region = this.regions[0]
    this.getUsers(this.type_tab_items[0]);
    this.selected_tab_item = this.fstatus
    this.users.search.selected_member_type = this.users.search.member_type_list[0].value
    this.users.search.selected_member_string = this.users.search.member_string_list[0].value
  },
  watch: {
    'users.options': {
      handler() {
        this.getUsers(this.type_tab_items[this.selected_tab_item])
      },
      deep: true
    },
    fstatus () {
      console.log('fstatus: ' + this.fstatus)
      this.selected_tab_item = this.fstatus
    }
  },
  data() {
    return {
      users: {
        selected: [],
        singleSelect: false,
        headers_user: [
          {text: 'No.', value: 'id', sortable: false,align: 'start', width: 60},
          {text: "사용자구분", value: "user_type",align: 'center', sortable: false},
          // {text: "지부", value: "area_code",align: 'center', sortable: true},
          {text: "아이디", value: "user_id",align: 'center', sortable: false},
          {text: "성명", value: "user_name",align: 'center', sortable: false},
          {text: "전화번호", value: "phone",align: 'center', sortable: false},
          {text: "핸드폰번호", value: "telephone",align: 'center', sortable: false},
          // {text: "부서", value: "dept_name",align: 'center', sortable: false},
          {text: "등록일자", value: "created_date",align: 'center', sortable: false},
          // {text: "회원상태", value: "user_status",align: 'center',width:200,sortable: true},
        ],
        headers_history: [
          { text: 'No.', value: 'id',align: 'center', sortable: false, width: 40 },
          { text: '일시', value: 'created',align: 'center', sortable: false, width: 180 },
          { text: '아이디', value: 'user_id',align: 'center', sortable: false },
          { text: '유형', value: 'type',align: 'center', sortable: false },
          { text: '아이피', value: 'ip_addr',align: 'center', sortable: false },
          { text: '운영체제', value: 'os_ver',align: 'center', sortable: false },
          { text: '브라우저', value: 'browser_ver',align: 'center', sortable: false },
        ],
        search_text: '',
        data: [],
        options: {},
        loading: false,
        search:{
          selected_user_type:null,
          selected_user_status:null,
          selected_member_type:null,
          selected_member_string:null,
          member_type_list:[
            {text:'전체',value:0},
            {text:'회원',value:1},
            {text:'학교',value:2}
          ],
          member_string_list:[
            {text:'전체',value:0},
            {text:'아이디',value:1},
            {text:'회원명',value:2},
            {text:'학교명',value:3},
            {text:'지역명',value:4},
          ],
        }

      },
      popup:{
        user: {
          data: {
            user_id:''
          },
          show: false,
          errors: [],
          form: {
            // user_id: "test01",
            // user_pw: "testtest01",
            // user_pwc: "testtest01",
            // user_name: "test01",
            // user_type: "2",
            // user_status: "",
            // phone: "test01",
            // email: "test01",
            // token: "",
            // last_logon_time: moment().format("YYYY-MM-DD"),
          },
          selected_area_type:null,
          selected_user_status:null,
          selected_user_region:null,
          selected_user_search_type:null,
          r_area_type:null,
          r_user_status:null,
          passwd:"",
          passwd_c:"",
          user_phone_1:'',
          user_phone_2:'',
          user_phone_3:'',
          user_telephone:'',
          user_telephone_1:'',
          user_telephone_2:'',
          user_telephone_3:'',
        },
        del_user:{
          show:false,
          del_item:null,
          errors: [],
        },
        deleted_user:{
          show:false,
          errors: [],
        }
      },
      member_user_type:[
        {name:'관리자',code:1,check:false},
        {name:'품질검사',code:2,check:false},
        {name:'오픈API',code:3,check:false},
      ],
      member_user_type_m:[
        {name:'전체',code:0,check:false},
        {name:'공제사업처',code:2,check:false},
        {name:'권역별 지부',code:3,check:false},
        {name:'일반',code:4,check:false},
      ],
      member_area_type:[
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_area_type_m:[
        {text:'전체',value:'R000',index:0},
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_user_status:[
        {text:'대기',value:1},
        {text:'승인',value:2}
      ],
      member_user_status_m:[
        {text:'전체',value:2},
        {text:'대기',value:0},
        {text:'승인',value:1}
      ],
      regions: [
        {value: 0, text: '전체'},
        {value: 1, text: '강원'},
        {value: 2, text: '경기'},
        {value: 3, text: '경남'},
        {value: 4, text: '경북'},
        {value: 5, text: '광주'},
        {value: 6, text: '대구'},
        {value: 7, text: '대전'},
        {value: 8, text: '부산'},
        {value: 9, text: '서울'},
        {value: 10, text: '세종'},
        {value: 11, text: '울산'},
        {value: 12, text: '인천'},
        {value: 13, text: '전남'},
        {value: 14, text: '전북'},
        {value: 15, text: '제주'},
        {value: 16, text: '충남'},
        {value: 17, text: '충북'}
      ],

      loading: false,
      selected_tab_item: null,
      type_tab_items: ['사용자'],
      all_item_check:true
    };
  },
};
</script>

<style lang="scss" scoped>
.main-panel {
  padding: 10px;
  height: calc(100vh - 80px);
  overflow-y: auto;
}
.datetime-wrap {
  position: relative;
}
.func-wrap {
  position: absolute;
  top: 10px;
  right: -200px;
  width: 200px;
}
.main-panel .v-data-table header {
  font-size: 14px;
}
.main-panel .v-data-table th {
  font-size: 14px;
}
.main-panel .v-data-table td {
  font-size: 14px;
}
.search-action {
  flex: 0 0 120px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.m-right{margin-right: 20px;}
.v-c-size{
  width:80px;
  height:5px;
  text-align: center;
  margin-top: -15px;
  margin-left:35px;
}
.v-l-size{
  font-size: 14px;
  width:40px;
  text-align: center;
  margin-top: 0px;
  margin-left: -10px;
}
.v-l-size-2{
  font-size: 14px;
  width:100px;
  text-align: center;
  margin-top: 0px;
  margin-left: -10px;
}
.v-c-size-h{
  width:80px;
  height:5px;
  text-align: center;
  margin-top: -15px;
  margin-left:0px;
}
td {
  text-align: center;
}

.user-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.user-close {
  position: absolute;
  top: 0px; right: 20px;
  z-index: 10;
}
.user-page {
  padding: 5px 5px;
  .th-cursor{
    cursor: pointer;
  }
}
.s-size{
  width:230px;
  max-height:20px !important;
  margin-top:-16px;
  margin-left:10px;
}
.s-left{
  text-align: left;
  margin-left: 0px;
}
.v-col-right{
  text-align: right;
}

.user-info-container {
  position: relative;
}
.user-info-close {
  position: absolute;
  top: 10px; right: 20px;
  z-index: 10;
}
</style>
