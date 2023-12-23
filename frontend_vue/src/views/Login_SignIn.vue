<template>
  <div>
    <div class="d-flex elevation-2 white">
      <div class="login-panel">
        <div class="login-panel-inner">
          <div class="login-legend">
<!--            <img src="@/assets/logo-black.png"/>-->
            <div class="login-legend-1">공공데이터 품질검사 지원 시스템</div>
          </div>
          <div class="login-input-wrap">

            <v-tabs-items v-model="tabs">
              <v-tab-item value="tab1">
                <div class="login-inner">
                  <v-form>
                    <div class="mb-4">
                      <v-text-field outlined dense hide-details
                        v-model="form.user_id"
                        label="아이디"
                        name="login"
                        type="text"
                        suffix=""
                        prepend-inner-icon="person"
                        @keypress.enter="login"
                      />
                    </div>
                    <div>
                      <v-text-field outlined dense hide-details
                        v-model="form.user_pw"
                        id="password"
                        label="비밀번호"
                        name="password"
                        prepend-inner-icon="lock"
                        type="password"
                        @keypress.enter="login"
                      />
                    </div>
                  </v-form>
                  <div class="d-flex justify-space-between align-start">
                    <v-checkbox dense :ripple="false" v-model="remember">
                      <template v-slot:label>
                        <span class="text-subtitle-2">아이디 저장</span>
                      </template>
                    </v-checkbox>
                  </div>
                  <v-btn block large depressed dark color="#0044CB" @click="login" :loading="loading">로그인</v-btn>
                  <v-divider class="mt-6 mb-3"/>
                </div>
              </v-tab-item>
              <v-tab-item value="tab2">
                <div class="login-inner">
                  <v-form>
                    <div class="mb-4">
                      <v-text-field outlined dense hide-details
                        v-model="form.user_id"
                        label="아이디"
                        name="login"
                        type="text"
                        prepend-inner-icon="person"
                        @keypress.enter="login"
                      />
                    </div>
                    <div>
                      <v-text-field outlined dense hide-details
                        v-model="form.user_pw"
                        id="password"
                        label="비밀번호"
                        name="password"
                        prepend-inner-icon="lock"
                        type="password"
                        @keypress.enter="login"
                      />
                    </div>
                  </v-form>
                  <div class="d-flex justify-space-between">
                    <v-checkbox dense v-model="remember">
                      <template v-slot:label>
                        <span class="text-subtitle-2">아이디 저장</span>
                      </template>
                    </v-checkbox>
                  </div>
                  <v-btn block large depressed dark color="#0044CB" @click="login" :loading="loading">로그인</v-btn>
                </div>
              </v-tab-item>
            </v-tabs-items>
          </div>
        </div>
      </div>

<!--      <div class="notice-wrap">-->
<!--        <div class="notice-header">-->
<!--          공지사항-->
<!--        </div>-->

<!--        <div class="py-3">-->
<!--          <div v-for="item in notices" :key="item.id" class="notice-list-item" @click="noticeDetailHandler(item)">-->
<!--            <div class="notice-list-item-title">{{item.title}}</div>-->
<!--            <div class="notice-list-item-date">{{item.created_date | moment('YYYY-MM-DD')}}</div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->

    </div>

    <v-dialog v-model="popup.show" max-width="480">
      <v-card v-if="popup.data">
        <v-card-title class="headline">{{popup.data.title}}</v-card-title>
        <v-card-text>
          <div class="notice-content">{{popup.data.contents}}</div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary darken-1" text  @click="popup.show = false">
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
export default {
  methods: {
    async login() {
      this.loading = true;
      try {
        if(this.tabs == 'tab1') this.form.login_type = 1
        else this.form.login_type = 2
        
        let {data} = await this.$http.post('login', this.form)
        if(data.status) {
          await this.$session.login(data);

          Cookies.set('lgntb', this.tabs)

          if (this.remember) Cookies.set('remb', this.form.user_id)
          else Cookies.set('remb', '')

          if (this.autologin) Cookies.set('atlg', 'Y')
          else Cookies.set('atlg', '')

          this.$router.replace({name: (this.$session.isAdmin())? 'ndp_user':'ndp_user'})
        }
        else {
           if(data.reason == 1 || data.reason == 2) {
             this.$session.$emit('modal-alert', '아이디 또는 비밀번호가 잘못 입력되었습니다.')
           }else if(data.reason == 3) {
             this.$session.$emit('modal-alert', '관리자 승인 후 사용 가능합니다.')
           }
        }
      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }
    },
    noticeDetailHandler (notice) {
      this.popup.data = notice
      this.popup.show = true
    }
  },
  mounted () {
    let remember = Cookies.get('remb')
    let autologin = Cookies.get('atlg')
    this.tabs = Cookies.get('lgntb') || 'tab1'
    

    if (remember) {
      this.remember = true
      this.form.user_id = remember
    }

    if (autologin === 'Y') {
      // 나중엔 자동 로그인 동작 추가
      this.autologin = true
    }
  },
  data() {
    return {
      loading: false,
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
      autologin: false,
      tabs: ''
    };
  }
};
</script>

<style lang="scss" scoped>
  .notice-content {
    white-space: pre-line;
  }
  .login-panel-inner {
    width: 380px;
  }
  .login-input-wrap {
  }
  .login-fn-btn {
    min-width: 100px;
    text-align: center;
  }
  .notice-wrap {
    padding: 48px;
    overflow: hidden;
    background-color: #DFEFF7;
    background-image: url(~@/assets/bg/bg-3.svg);
    background-size: contain;
    background-position: left bottom;
    flex: 1 1 50%;
  }
  .notice-header {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: bold;
    font-size: 16px;
    line-height: 23px;
    letter-spacing: -0.04em;

    padding-bottom: 10px;
    border-bottom: 1px solid white;
  }
  .notice {
    // 배경을 넣으시려면 이부분 주석을 해제하시면 됩니다
    // background-image: url(../assets/bg/bg-1.jpg);
    // background-size: cover;
    // background-position: center center;
  }
  .cloud-img {
    width: 538px;
  }
  .login-panel {
    overflow: hidden;
    flex: 1 1 50%;
    padding: 60px 0;
    min-width: 500px;
    display: flex;
    justify-content: center;
    align-items: center;

  }
  .login-legend {
    text-align: center;
    margin-left: -40px;
    margin-bottom: 40px;
  }
  .login-legend-1 {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: bold;
    font-size: 24px;
    line-height: 35px;
    letter-spacing: -0.04em;
  }
  .login-legend-2 {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: normal;
    font-size: 12px;
    line-height: 17px;
  }
  .v-list-w{
    max-width: 300px;
  }
  .disabled {
    opacity: 0.5;
    pointer-events: none;
  }


  .notice-list-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 4px 0;
    padding-left: 12px;

    font-size: 12px;
    color: #404040;

    cursor: pointer;
    position: relative;
  }
  .notice-list-item-title {
    &:before {
      position: absolute;
      content: "•";
      font-size: 18px;
      top: 9px; left: 0px;
      line-height: 0;
    }
  }
  .notice-list-item-date {
    font-size: 11px;
  }

</style>
