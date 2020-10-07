import React, { Component } from 'react'
import Taro from '@tarojs/taro'
import { View, Button, Image, Text } from '@tarojs/components'
import './game.less'

export default class Game extends Component {
  constructor(props) {
    super(props);
    this.state={
      nickName:"游客",
      avatarUrl:"",
      level: 0
    }
  }

  componentWillMount () {
    var that = this;
    Taro.getUserInfo({
      success: function(res) {
        var userInfo = JSON.parse(res.rawData);
        that.setState({
          nickName: userInfo.nickName,
          avatarUrl: userInfo.avatarUrl
        })
    ;}});
  }

  componentDidMount () {
  }

  componentWillUnmount () { }

  componentDidShow () { }

  componentDidHide () { }

  

  render () {
    return (
      <View className='frame'>
        <View className='personal_info'>
          <Image src={this.state.avatarUrl} className='image'>
          
          </Image>
          <View className='personal_info_text'>
            <Text>
              {this.state.nickName}
            </Text>
            <Text>
              Level {this.state.level}
            </Text>
          </View>
          
        </View>
      </View>
    )
  }
}
