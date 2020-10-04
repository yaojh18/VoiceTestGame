import React, { Component } from 'react'
import Taro from '@tarojs/taro'
import { View, Button } from '@tarojs/components'
import './index.less'

export default class Index extends Component {

  componentWillMount () { }

  componentDidMount () { }

  componentWillUnmount () { }

  componentDidShow () { }

  componentDidHide () { }

  DeliverUserInfo (e) {
    console.log(e.userInfo);
    Taro.switchTab({url:"../game/game"});
  }

  render () {
    return (
      <View className='frame'>
        <Button
          className='button'
          open-type='getUserInfo'
          onGetUserInfo={this.DeliverUserInfo.bind(this)}
        >
          开始游戏
        </Button>
      </View>
    )
  }
}
