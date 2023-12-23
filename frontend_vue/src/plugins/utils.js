import _ from 'lodash'
import numeral from 'numeral'

const regx_end_session = /^Ended\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*),\s(\d+)\s(.*)$/
const regx_start_remote = /^Started\sremote\sdesktop\swithout\snotification\s\((.*)\)$/
const regx_start_session = /^Started\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*)$/

export default {
  install(Vue) {
    Vue.filter('format', (value, option) => {
      if (!option) option = '0,0'
      return numeral(value).format(option)
    })
    Vue.prototype.$numeral = numeral

    Vue.prototype.$getColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'cost_color_1'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'cost_color_2'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'cost_color_3'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'cost_color_4'
      else
        return 'cost_color_5'
    }
    Vue.prototype.$getLevel = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 1
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 2
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 3
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 4
      else
        return 5
    }
    Vue.prototype.$getCostColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'cost_color_1'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'cost_color_2'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'cost_color_3'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'cost_color_4'
      else
        return 'cost_color_5'
    }

    Vue.prototype.$getCostRange = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return '1천만원 미만'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return '1천만원 ~ 2천만원'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return '3천만원 ~ 5천만원'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return '5천만원 ~ 1억원'
      else
        return '1억원이상'
    }

    Vue.prototype.$getTextColor = (cost) => {
      var cost_array = [10000000, 20000000, 50000000, 100000000]
      if (cost < cost_array[0])
        return 'blue--text'
      else if (cost >= cost_array[0] && cost <= cost_array[1])
        return 'amber--text'
      else if (cost >= cost_array[1] && cost <= cost_array[2])
        return 'yellow--text'
      else if (cost >= cost_array[2] && cost < cost_array[3])
        return 'deep-orange--text'
      else
        return 'red--text'
    }

  }
}
