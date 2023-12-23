<template>
  <div class="w-100">
    <v-app-bar app clipped-left dense class="top-menu" color="white" elevation="1">
      <div class="ml-auto d-flex align-center">
        <v-divider vertical/>
        <v-btn  text color="grey darken-1" href="" @click="userinfo.show=true">
          <v-icon color="grey lighten-1" class="mr-1">mdi-account-edit</v-icon>
          {{getLoginName()}}
        </v-btn>
        <v-divider vertical/>
        <v-btn icon small color="deep-orange accent-2" class="ml-4" @click="logout_dialog.show=true">
          <v-icon>mdi-power</v-icon>
        </v-btn>
      </div>
    </v-app-bar>


    <v-navigation-drawer class="m-top-20" app permanent color="#eceff0" :mini-variant="mini">
      <div class="mt-2 px-4 d-flex justify-space-between align-center">
        <template v-if="mini">
          <v-icon @click="mini = false">mdi-chevron-double-right</v-icon>
        </template>
        <template v-else>
          <v-btn icon @click="mini = true">
            <v-icon>mdi-chevron-double-left</v-icon>
          </v-btn>
        </template>
      </div>
      <v-list class="py-0">
        <v-list-item v-if="$session.isAdmin()" v-once :to="{name: navLinks[5].subLinks[0].route}" color="primary">
          <v-list-item-avatar>
            <v-icon>{{navLinks[5].icon}}</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{navLinks[5].text}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <div v-if="$session.isAdmin()" class="subMenuWrapper">
          <v-list class="py-0 subMenu" :class="{subMenuOpen: $route.path.startsWith('/ndp_user')}">
            <v-list-item dense :to="{name: navLinks[5].subLinks[0].route}" color="primary lighten-2">
              <v-list-item-content>
                <v-list-item-title class="pl-14">{{navLinks[5].subLinks[0].text}}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>        
          </v-list>
        </div>
     
      </v-list>

      
    </v-navigation-drawer>
    <v-main class="page-container">
      <slot></slot>
    </v-main>
    <v-dialog v-model="userinfo.show" persistent max-width="1000px" max-height="500px">
      <div class="user-info-container">
        <v-btn fab x-small dark depressed color="grey darken-1" class="user-info-close" @click="userinfo.show=false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <user-info :userinfo="$session.getUserInfo()" :call_type="{myinfo:true,regist:false,userlist_add:false,userlist_modify:false}"/>
      </div>
    </v-dialog>
    <v-dialog v-model="logout_dialog.show" max-width="500px">
      <v-card>
        <v-card-title>로그아웃 하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="$session.logout()">로그아웃</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="logout_dialog.show = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import UserInfo from '@/components/UserInfo'
import axios from "axios";
export default {
  components: {UserInfo},
  props: {
    source: String,
  },
  methods:{
    move_page(move_info){
      if (move_info.name === this.$route.name && move_info.params.fstatus === this.$route.params.fstatus) {
        return;
      }
      else {
        this.$router.push(move_info)
      }
    },
    move_page_to(sub){
      this.$router.push(sub.route)
    },
    getLoginName(){
      return this.$session.getUserName()
    },
  },
  computed: {
  },
  mounted () {
  },
  data: () => ({
    groupOpened:true,
    mini: false,
    worktime: '00:00',
    refreshKey: Date.now(),
    navLinks: [
      {
        icon: "mdi-solar-panel-large",
        text: "사업관리",
        subLinks: [
          { text: "사업목록", route: "ndp_base_manage"},
          { text: "과제목록", route: "ndp_task_manage"},
          { text: "공급기업목록", route: "ndp_scom_manage"},
          { text: "수요기관목록", route: "ndp_govm_manage"},
        ]
      },
      {
        icon: "mdi-movie-roll",
        text: "과제관리",
        subLinks: [
          { text: "과제조회", route: "ndp_task_dashboard"},
          { text: "파일관리", route: "ndp_task_file_manage"},
          { text: "과제수행이력", route: "ndp_task_hist_manage"},
          { text: "과제첨부파일", route: "ndp_task_attatch" },
        ]
      },
      {
        icon: "mdi-movie-roll",
        text: "품질관리",
        subLinks: [
          { text: "품질현황", route: "ndp_task_status_manage"},
          { text: "품질검사결과", route: "ndp_task_status_result"},
          { text: "품질업로드파일(샘플)", route: "ndp_task_status_sample_upload" },
          { text: "품질업로드파일", route: "ndp_task_status_upload" },
        ]
      },
      {
        icon: "mdi-movie-roll",
        text: "OPEN API",
        subLinks: [
          { text: "OPENAPI 업로드파일", route: "ndp_task_openapi_upload"}
        ]
      },      
      {
        icon: "mdi-battlenet",
        text: "통계",
        subLinks: [
          { text: "과제현황통계", route: "ndp_task_status_static"},
          // { text: "파일현황통계", route: "ndp_task_file_static"},
          // { text: "과제수행이력통계", route: "ndp_task_hist_static"},
        ]
      },
      {
        icon: "mdi-account-convert",
        text: "사용자 관리",
        subLinks: [
          { text: "사용자", route: "user_manage"},
          { text: "사용자 접속이력", route: "ndp_user_hist"},
        ]
      },
      {
        icon: "mdi-account-convert",
        text: "커뮤니티",
        subLinks: [
          { text: "게시판", route: "ndp_community_board"},
        ]
      },
    ],

    sitemap_dialog:{
      show:false
    },
    userinfo: {
      show: false,
      data: null
    },
    logout_dialog: {
      show: false,
    },
    smtp_dialog:{
      show:false,
      form:{
        smtp_server:'',
        smtp_port:null,
        smtp_sender:'',
        smtp_id:'',
        smtp_pass:''
      }

    },
  }),
};
</script>

<style lang="scss">
/* #keep .v-navigation-drawer__border {
  display: none
} */
.top-menu {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
}
.float-menu {
  position: absolute;
  width: 300px;
  z-index: 100;

  &.fm-main {
    top: 63px;
    left: 5px;
  }
  &.fm-sub {
    top: 15px;
    left: 5px;
  }
}
.page-container {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
  background-color:#dadada;
  // background-color: #3d5f70;
  // background-image: url(../assets/bg/bg-1.jpg);
  // background-size: cover;
}
.inc-count {
  display: inline-block;
  margin: 4px 0px 4px 5px;
  box-sizing: border-box;
  font-weight: bold;
}

.sub-menu {
  border-radius: 5px;
  // background-color: rgba(21, 65, 106, 0.8);
  background-color: rgba(255,255,255,0.86);
}

.menusd-enter-active {
  position: absolute;
  transition: transform 0.5s;
}
.menusd-leave-active {
  position: absolute;
  transition: transform 0.5s;
}
.menusd-enter {
  transform: translateX(-320px);
}
.menusd-leave-to {
  transform: translateX(-320px);
}
.sitemap-container {
  position: relative;
}
.sitemap-close {
  position: absolute;
  top: 2px; right: 10px;
  z-index: 10;
}
.sitemap-page {
  padding: 5px 5px;
  .th-cursor{
    cursor: pointer;
    margin-left: 10px;
    border-bottom: 1px solid blueviolet;
  }
}

.main-menu-header {
  height: 30px !important;
  background-color: #2a5b82;
  border-color: #2a5b82;
  color: white !important;
}

.breadcrumb {
  background-color: white;
  border-bottom: 1px solid #dadada;
}
.sw-pos {
  margin-top: -12px;
}

.user-info-container {
  position: relative;
}
.user-info-close {
  position: absolute;
  top: 10px; right: 20px;
  z-index: 10;
}
.v-pos {
  position: absolute;
  top: 50px; left: 100px;
}

.page-enter-active,
.page-leave-active {
  position: absolute;
  width: calc(100vw - 256px);
  transition: transform 0.85s ease, left 0.85s ease;
}
.page-enter {
  left: -100%;
}
.page-enter-to {
  left: 0%;
}
.page-leave {
  transform: scale(1);
}
.page-leave-to {
  transform: scale(0.8);
}

.subMenuWrapper {
  position: relative;
  overflow-x: hidden;
}
.subMenu {
  margin-top: -320px;
  transition: margin-top 0.25s;
}
.subMenu.subMenuOpen { margin-top: 0; }
.m-top-20{
  margin-top: 50px;
}
.btn-bottom-layer{
  margin-top: 100px;
  text-align: center;
}
.btn-bottom-layer-b{
  margin-top: 10px;
  text-align: center;
}
</style>
