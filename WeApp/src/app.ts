import { Component } from 'react'
import Taro from '@tarojs/taro'
import './app.less'

class App extends Component {
  globalData: {user_id: 0}

  componentDidMount () {
    let that = this;
    Taro.login({
      success: function (res) {
        if (res.code) {
          //发起网络请求
          Taro.request({
            url: '',
            method: "POST",
            data: {
              code: res.code
            },
            success:function (res) {
              that.globalData.user_id = res.data.user_id;
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  }

  componentDidShow () {}

  componentDidHide () {}

  componentDidCatchError () {}

  // this.props.children 是将要会渲染的页面
  render () {
    return this.props.children
  }
}

export default App
