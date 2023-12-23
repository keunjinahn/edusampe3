import axios from 'axios'

let sessionToken = sessionStorage.getItem('sessionToken')
let commonHeader = {}
if (sessionToken) {
  commonHeader.token = sessionToken
}

const http = axios.create({
  baseURL: `/api/monitor/${process.env.VUE_APP_API_MONITOR_VER}`,
  timeout: 50 * 1000,
  headers: {
    common: commonHeader
  }
})

http.interceptors.request.use(
  (config) => {
    if (!config.params) config.params = {}
    // config.params._cache = Date.now()
    return config
  },
  (error) => {
    return Promise.reject(error);
  }
)

const ndpApi = axios.create({
  baseURL: `/api/ndp/${process.env.VUE_APP_API_MONITOR_VER}`,
  timeout: 50 * 1000,
  headers: {
    common: commonHeader
  }
})

ndpApi.interceptors.request.use(
  (config) => {
    if (!config.params) config.params = {}
    return config
  },
  (error) => {
    return Promise.reject(error);
  }
)


export default {
  install(Vue) {
    Vue.prototype.$http = http
    Vue.prototype.$http_ndp = ndpApi
  }
}

export { http, ndpApi }
