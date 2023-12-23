<template>
  <v-card class="elevation-12 vc-pos">
    <template v-if="step === 0">
      <v-subheader>약관에 동의해 주세요</v-subheader>
      <v-divider/>
      <div class="pa-6">
        <div class="term-title">1. 이용약관</div>
        <div class="term-preview">
          <agmt-use />
        </div>
        <v-checkbox label="약관에 동의합니다" v-model="agreements[0]"/>
      </div>
      <v-divider/>
      <div class="d-flex justify-space-between">
        <v-btn depressed text large @click="$router.push({name: 'login'})">
          <v-icon>mdi-close</v-icon>
          <div class="ml-1 line-height-hangul-fix">취소</div>
        </v-btn>
        <v-btn depressed text large
          color="primary"
          :disabled="!(agreements[0])"
          @click="step = 1">
          <div class="mr-1 line-height-hangul-fix">다음</div>
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </div>
    </template>
    <template v-if="step === 1">
      <v-subheader>약관에 동의해 주세요</v-subheader>
      <v-divider/>
      <div class="pa-6">
        <div class="term-title">2. 개인정보 수집 및 이용</div>
        <div class="term-preview">
          <agmt-privacy />
        </div>
        <v-checkbox label="약관에 동의합니다" v-model="agreements[1]"/>
      </div>
      <v-divider/>
      <div class="d-flex justify-space-between">
        <v-btn depressed text large @click="$router.push({name: 'login'})">
          <v-icon>mdi-close</v-icon>
          <div class="ml-1 line-height-hangul-fix">취소</div>
        </v-btn>
        <v-btn depressed text large
               color="primary"
               :disabled="!(agreements[1])"
               @click="step = 2">
          <div class="mr-1 line-height-hangul-fix">다음</div>
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </div>
    </template>
    <template v-if="step === 2">
      <v-subheader>약관에 동의해 주세요</v-subheader>
      <v-divider/>
      <div class="pa-6">
        <div class="term-title">3. 위치정보 이용약관</div>
        <div class="term-preview">
          <agmt-location />
        </div>
        <v-checkbox label="약관에 동의합니다" v-model="agreements[2]"/>

      </div>
      <v-divider/>
      <div class="d-flex justify-space-between">
        <v-btn depressed text large @click="$router.push({name: 'login'})">
          <v-icon>mdi-close</v-icon>
          <div class="ml-1 line-height-hangul-fix">취소</div>
        </v-btn>
        <v-btn depressed text large
               color="primary"
               :disabled="!(agreements[2])"
               @click="step = 3">
          <div class="mr-1 line-height-hangul-fix">다음</div>
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </div>
    </template>
    <template v-else-if="step === 3">
      <user-info class="u-width" :call_type="{myinfo:false,regist:true,userlist_add:false,userlist_modify:false}"/>
    </template>
    <template v-else-if="step === 4">
      <div class="px-6 py-10 text-center">
        <div class="mb-6 text-h4 font-weight-thin text-center">
          관리자가 승인하면 <br>가입이 완료됩니다
        </div>
        <v-btn text large color="primary" @click="$router.push({name: 'login'})">
          로그인 화면으로 이동
        </v-btn>
      </div>
    </template>
<!--    <template v-else>-->
<!--      잘못된 접근입니다-->
<!--    </template>-->
  </v-card>
</template>

<script>
import Cookies from 'js-cookie'
import UserInfo from '@/components/UserInfo'
import {AgmtUse, AgmtLocation, AgmtPrivacy} from '@/components/Agreement'
export default {
  components: {UserInfo, AgmtUse, AgmtLocation, AgmtPrivacy},
  methods: {
    async getNotice () {
      let q = JSON.stringify({
        order_by: [{field: 'NOTICE_DT', direction: 'desc'}]
      })
      let params = {q, results_per_page: 5, page: 1}
      let {data} = await this.$http.get('notices', {params})
      this.notices = data.objects
    },

    async login() {
      this.loading = true;
      try {
        let {data} = await this.$http.post('login', this.form)
        await this.$session.login(data);

        if (this.remember) Cookies.set('remb', this.form.user_id)
        else Cookies.set('remb', '')

        this.$router.replace({name: 'ndp_task_dashboard'})
      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }
    },
    noticeDetailHandler (notice) {
      this.popup.data = notice
      this.popup.show = true
    },

    onUserTypeChage(index){
      this.member_user_type.forEach(v => v.check = false)
      this.member_user_type[index].check = true
    },
    onChangeAreaType(){
      this.user.r_area_code=this.user.selected_area_type
    },
    onChangeUserStatus(){
      this.user.r_user_status=this.user.selected_user_status
    },
    init_data(){
      this.user.selected_area_type = this.member_area_type[0]
      this.user.r_area_code = this.member_area_type[0].value
      this.member_user_type[1].check = true

    },
    async onUserOverlabCheck(){
      if(this.user.user_id_.length < 4){
        this.$session.$emit('modal-alert', '사용자 아이디(영문4자이상)를 입력해 주세요!')
        return
      }
      this.loading = true;
      try {
        let params = {user_id: this.user.user_id_}
        let {data} = await this.$http.post('login_overlap',params )
        if(data.status == true){
          if(data.overlap_result == 0){
            this.$session.$emit('modal-alert', '사용할 수 없는 아이디 입니다!')
            return
          }else{
            this.$session.$emit('modal-alert', '사용할 수 있는 아이디 입니다!')
          }
          this.overlab_result = data.overlap_result
        }
      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }
    },
    async submitAddMember () {
      if(this.overlab_result == 0){
        this.$session.$emit('modal-alert', '사용자 아이디 중복체크를 해주세요!')
        return
      }
      if(this.user.user_id_.length < 4){
        this.$session.$emit('modal-alert', '사용자 아이디(영문4자이상)를 입력해 주세요!')
        return
      }

      if (!this.user.user_passwd){
        this.$session.$emit('modal-alert', '비밀번호를 입력해 주세요!')
        return
      }
      else {
        if (this.user.user_passwd.length < 8){
          this.$session.$emit('modal-alert', '비밀번호는 8자 이상 길이여야 합니다.')
          return
        }
        if (!/^[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]+$/.test(this.user.user_passwd)) {
          this.$session.$emit('modal-alert', '비밀번호는 영문, 숫자, 특수문자를 포함해야 합니다.')
          return
        }
        if (this.user.user_passwd !== this.user.user_passwdc){
          this.$session.$emit('modal-alert', '비밀번호 확인과 일치하지 않습니다.')
          return
        }
      }
      if(this.user.user_name.length < 2){
        this.$session.$emit('modal-alert', '사용자 이름(2자이상)을 입력해 주세요!')
        return
      }
      if(this.user.dept_name.length < 2){
        this.$session.$emit('modal-alert', '부서명을 입력해 주세요!')
        return
      }

      this.loading = true;
      try {
        let params = {}
        params.user_id = this.user.user_id_;
        params.user_pw = this.user.user_passwd;
        params.user_name = this.user.user_name;
        for(var i=0;i<this.member_user_type.length;i++){
          if(this.member_user_type[i].check == true) {
            params.user_type = i+1
            break
          }
        }
        params.area_code = this.user.r_area_code
        params.user_status = 0
        params.phone = this.user.user_phone_1.toString() + '-' + this.user.user_phone_2.toString() + '-' + this.user.user_phone_3.toString();
        params.telephone = this.user.user_telephone_1.toString() + '-' + this.user.user_telephone_2.toString() + '-' + this.user.user_telephone_3.toString();
        params.dept_name = this.user.dept_name;
        let {data} = await this.$http.post('user_register',params )
        if(data.status == true){
            this.$session.$emit('modal-alert', '등록되었습니다.')
            this.step = 2
        }else{
          this.$session.$emit('modal-alert', '등록 실패하였습니다.')
        }
      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }

    },
  },
  mounted() {
    this.init_data()
  },
  data() {
    return {
      checkbox: true,
      show1: false,
      show2: true,
      show3: false,
      show4: false,
      password: 'Password',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        emailMatch: () => (`The email and password you entered don't match`),
      },
      loading: false,
      step: 0,
      agreements: [false, false, false],

      form: {
        user_id: "",
        user_pw: ""
      },
      notices: [],
      popup: {
        show: false,
        data: null
      },
      remember: false,
      user: {
        show: true,
        user_id_:'',
        user_name:'',
        dept_name:'',
        user_passwd:'',
        user_passwdc:'',
        user_phone:'',
        user_phone_1:'',
        user_phone_2:'',
        user_phone_3:'',
        user_telephone:'',
        user_telephone_1:'',
        user_telephone_2:'',
        user_telephone_3:'',
        user_email:'',
        errors: [],
        selected_area_type:null,
        selected_user_status:null,
        r_area_type:null,
        r_user_status:null,
        overlab_result:0
      },
      member_user_type:[
        {name:'관리자',code:1,check:false},
        {name:'공제사업처',code:2,check:false},
        {name:'권역별 지부',code:3,check:false},
        {name:'일반',code:4,check:false},
        {name:'회원',code:5,check:false},
        {name:'학교',code:6,check:false},
      ],
      member_area_type:[
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_user_status:[
        {text:'대기',value:0},
        {text:'승인',value:1}
      ],
    };
  }
};
</script>

<style lang="scss" scoped>
  .login-container {
    position: relative;
  }
  .login-title {
    position: absolute;
    top: -100px; left: -32px;
    background-color: white;
    font-size: 40px;
    padding: 2px 20px;
    font-weight: 100;
  }
  .term-preview {
    // padding: 10px;
    border: 1px solid #606060;
    font-size: 10px;
    overflow-x: hidden;
    overflow-y: scroll;
    height: 500px;
  }

  .report-cont {
    height: 100vh;
    margin-left:20px;
    overflow-y: auto;

    .report-inner {
      padding: 0px 10px;
    }

    &::-webkit-scrollbar { width: 2px; }
    &::-webkit-scrollbar-thumb { background-color: rgba(0,0,0,0.2); }
  }

  .user-info-close {
    position: absolute;
    top: 10px; right: 0px
  }
  .u-width{
    width: 800px;
  }
  .vc-pos{
    width: 1000px;
  }
</style>
