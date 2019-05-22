(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{208:function(e,t,a){},209:function(e,t,a){"use strict";a.r(t);var n=a(0),l=a.n(n),r=a(27),i=a.n(r),s=a(16),o=a(17),c=a(19),d=a(18),u=a(20),h=(a(93),a(94),a(15)),m=a.n(h),p=a(73),_=a.n(p),b=a(87),E=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(c.a)(this,Object(d.a)(t).call(this,e))).state={error:null,rose:0},a.displayed={rose:-1,cts:-1,heading:-1},a}return Object(u.a)(t,e),Object(o.a)(t,[{key:"updateSVGCompass",value:function(){var e=this.props,t=e.heading,a=e.cts,n=this.state.rose;if(t!==this.displayed.heading){var l=document.getElementById("compass_heading");l&&(console.log(l),l.setAttribute("transform","rotate("+t+")"),l.setAttribute("transform-origin","50% 50%"),this.displayed.heading=t)}if(a!==this.displayed.cts){var r=document.getElementById("compass_course");r&&(console.log(r),r.setAttribute("transform","rotate("+a+")"),r.setAttribute("transform-origin","50% 50%"),this.displayed.cts=a)}if(n!==this.displayed.rose){var i=document.getElementById("compass_rose");i&&(console.log(i),i.setAttribute("transform","rotate("+n+")"),i.setAttribute("transform-origin","50% 50%"),this.displayed.rose=n)}}},{key:"render",value:function(){return this.updateSVGCompass(),l.a.createElement("div",{className:"App-Compass"},l.a.createElement(b.a,{src:_.a}))}}]),t}(n.Component),v=a(21),g=a.n(v),C=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(c.a)(this,Object(d.a)(t).call(this,e))).handleCTSSliderChange=function(e,t){a.setState({cts_slider_value:t}),a.conditionSetCTS(3.6*(t-50)),a.postCts()},a.handleTrimSliderChange=function(e,t){a.setState({trim_slider_value:t});var n=(t-50)/10+a.state.cts_slider_value-50;a.conditionSetCTS(3.6*n),a.postCts()},a.state={error:null,isLoaded:!1,updated:!1,cts:0,heading:0,rose:0,cts_slider_value:50,trim_slider_value:50},a.url="http://192.168.1.126:8079/api/orientation",a.set_cts=0,a.local_control=0,a.local_control_count_down=3,a}return Object(u.a)(t,e),Object(o.a)(t,[{key:"getCompass",value:function(){var e=this;fetch(this.url).then(function(e){return e.json()}).then(function(t){e.setState({isLoaded:!0,updated:!0,cts:t.cts,heading:t.heading,pitch:t.pitch,roll:t.roll,calibration:t.calibration})},function(t){e.setState({isLoaded:!0,updated:!1,error:t})})}},{key:"postCts",value:function(){var e=this;fetch(this.url,{method:"post",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({cts:this.set_cts})}).then(function(e){return e.json()}).then(function(t){e.local_control=e.local_control_count_down,e.setState({isLoaded:!0,updated:!0,cts:t.cts,heading:t.heading})})}},{key:"componentDidMount",value:function(){var e=this;this.timer=setInterval(function(){e.getCompass(),e.set_cts!==e.state.cts&&(e.local_control>0?e.local_control--:e.setCTS(e.state.cts))},250)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"conditionSetCTS",value:function(e){e<0&&(e=360+e),e>360&&(e-=360),this.set_cts=Math.round(e)}},{key:"setCTS",value:function(e){this.conditionSetCTS(e);var t=Math.round(this.set_cts/3.6+50);t<0&&(t=100+t),t>100&&(t-=100),this.setState({cts_slider_value:t})}},{key:"render",value:function(){var e,t=this,a=this.state,n=a.cts_slider_value,r=a.cts,i=a.trim_slider_value,s=this.state.heading;return s=Math.round(s),e=this.state.updated?l.a.createElement(E,{cts:this.set_cts,heading:this.state.heading}):l.a.createElement("paper",null,l.a.createElement("h2",null,"No Communication: ",this.url)),l.a.createElement("div",null,l.a.createElement("div",{className:"pad"},e),l.a.createElement("div",{className:"pad"},l.a.createElement("h3",null,"Heading ",l.a.createElement("b",null,s)," M \xa0\xa0 \xa0CTS ",l.a.createElement("b",null,r)," M"),l.a.createElement("h4",null,"Course to Steer: "),l.a.createElement("div",null,l.a.createElement("span",{className:"floatLeft"},l.a.createElement(g.a,{color:"primary",onClick:function(){t.setCTS(t.set_cts-85),t.postCts()}},"-85"),l.a.createElement(g.a,{color:"primary",onClick:function(){t.setCTS(t.set_cts-5),t.postCts()}},"-5")),l.a.createElement("span",{className:"floatRight"},l.a.createElement(g.a,{color:"primary",onClick:function(){t.setCTS(t.set_cts+5),t.postCts()}},"+5"),l.a.createElement(g.a,{color:"primary",onClick:function(){t.setCTS(t.set_cts+85),t.postCts()}},"+85")),l.a.createElement(m.a,{value:n,"aria-labelledby":"set cts",onChange:this.handleCTSSliderChange})),l.a.createElement("br",null)," ",l.a.createElement("br",null),l.a.createElement("h4",null,"Trim Course:"),l.a.createElement(m.a,{value:i,"aria-labelledby":"trim course",onChange:this.handleTrimSliderChange}),l.a.createElement("br",null),l.a.createElement(g.a,{size:"small",color:"primary",onClick:function(){t.local_control=t.local_control_count_down;var e=.36*(i-50);t.setCTS(t.set_cts-e),t.state.trim_slider_value=50,t.setState({trim_slider_value:50})}},"Keep"),l.a.createElement(g.a,{size:"small",color:"primary",onClick:function(){t.conditionSetCTS(3.6*(n-50)),t.postCts(),t.state.trim_slider_value=50,t.setState({trim_slider_value:50})}},"Return")))}}]),t}(n.Component),f=a(23),S=a.n(f),k=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(c.a)(this,Object(d.a)(t).call(this,e))).handleKpSliderChange=function(e,n){var l=t.relativePerCent(n,a.state.slider_kd,a.state.slider_ki);n=l[0];var r=l[1],i=l[2];a.setState({slider_kp:n,slider_kd:r,slider_ki:i}),a.postCalibration()},a.handleKdSliderChange=function(e,n){var l=t.relativePerCent(n,a.state.slider_kp,a.state.slider_ki);n=l[0];var r=l[1],i=l[2];a.setState({slider_kp:r,slider_kd:n,slider_ki:i}),a.postCalibration()},a.handleKiSliderChange=function(e,n){var l=t.relativePerCent(n,a.state.slider_kp,a.state.slider_kd);n=l[0];var r=l[1],i=l[2];a.setState({slider_kp:r,slider_kd:i,slider_ki:n}),a.postCalibration()},a.handleGainSliderChange=function(e,t){t=Math.round(t);var n=(t=Math.max(t,5))*a.state.gain_slider_multiplier;a.setState({slider_gain:t,max_value:n}),a.postCalibration()},a.handleRudderRateSliderChange=function(e,t){var n=(t/a.rudder_rate_scale).toFixed(2);a.setState({slider_rudder_rate:t,rudder_rate:n}),a.postCalibration()},a.state={error:null,isLoaded:!1,updated:!1,kp:0,kd:0,ki:0,gain:0,rudder_rate:0,set_cal:0,slider_kp:0,slider_ki:0,slider_kd:0,slider_gain:0,slider_rudder_rate:0,gain_slider_multiplier:12},a.url="http://192.168.1.126:8079/api/calibration",a.can_update=!0,a.rudder_rate_scale=50,a}return Object(u.a)(t,e),Object(o.a)(t,[{key:"setCalibrationState",value:function(e){var t=e.kp,a=e.kd,n=e.ki,l=t+a+n,r=100/(l=Math.max(l,15));console.log(l,r),this.setState({isLoaded:!0,updated:!0,kp:t,kd:a,ki:n,rudder_rate:e.rudder_rate,max_value:l,slider_kp:Math.round(t*r),slider_kd:Math.round(a*r),slider_ki:Math.round(n*r),slider_gain:Math.round(l/this.state.gain_slider_multiplier),slider_rudder_rate:Math.round(e.rudder_rate*this.rudder_rate_scale),set_cal:e.set_cal,calibration:e.calibration})}},{key:"getCalibration",value:function(){var e=this;fetch(this.url).then(function(e){return e.json()}).then(function(t){e.setCalibrationState(t)},function(t){e.setState({isLoaded:!0,updated:!1,error:t})})}},{key:"postCalibration",value:function(){var e=this;this.can_update&&(this.can_update=!1,setTimeout(function(){fetch(e.url,{method:"post",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({kp:e.state.slider_kp*e.state.max_value/100,kd:e.state.slider_kd*e.state.max_value/100,ki:e.state.slider_ki*e.state.max_value/100,rudder_rate:e.state.rudder_rate,set_cal:e.set_cal})}).then(function(e){return e.json()}).then(function(t){e.setCalibrationState(t),e.can_update=!0})},1e3))}},{key:"componentDidMount",value:function(){this.getCalibration()}},{key:"render",value:function(){var e=this.state,t=e.slider_kp,a=e.slider_kd,n=e.slider_ki,r=e.slider_gain,i=e.slider_rudder_rate;return this.state.updated?l.a.createElement("div",null,l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Relative Kp: ",t,"%"),l.a.createElement(m.a,{value:t,"aria-labelledby":"set kp",onChange:this.handleKpSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Relative Kd: ",a,"%"),l.a.createElement(m.a,{value:a,"aria-labelledby":"set kd",onChange:this.handleKdSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Relative Ki: ",n,"%"),l.a.createElement(m.a,{value:n,"aria-labelledby":"set ki",onChange:this.handleKiSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"K Value at 100%: ",r*this.state.gain_slider_multiplier),l.a.createElement(m.a,{value:r,"aria-labelledby":"set ki",onChange:this.handleGainSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Drive Rudder Rate: ",(i/this.rudder_rate_scale).toFixed(2)," degrees per second"),l.a.createElement(m.a,{value:i,"aria-labelledby":"set rudder rate",onChange:this.handleRudderRateSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement(S.a,null,l.a.createElement("h3",null,"Compass/Orientation Chip Calibration:"),l.a.createElement(g.a,{variant:"contained",size:"small",color:"primary",onClick:function(){}},"Erase"),"\xa0\xa0\xa0\xa0\xa0\xa0",l.a.createElement(g.a,{variant:"contained",size:"small",color:"primary",onClick:function(){}},"Store"),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("br",null))):l.a.createElement("paper",null,l.a.createElement("h2",null,"No Communication: ",this.url))}}],[{key:"relativePerCent",value:function(e,t,a){var n=(100-e)/((t+=.5)+(a+=.5));return[e=Math.round(e),t=Math.round(t*n),a=Math.round(a*n)]}}]),t}(n.Component),y=a(79),j=a(80),O=a.n(j),w=a(81),x=a.n(w),M=a(82),T=a.n(M),N=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(c.a)(this,Object(d.a)(t).call(this,e))).handleSpeedSliderChange=function(e,t){var n=(t/a.speed_scale).toFixed(1);a.setState({slider_speed:t,speed:n}),a.postSimulation()},a.handlePowerBiasSliderChange=function(e,t){var n=((t-=50)/a.power_bias_scale*10).toFixed(0);a.setState({slider_power_bias:t,power_bias:n}),a.postSimulation()},a.handleGainSliderChange=function(e,t){var n=(t/a.gain_scale).toFixed(0);a.setState({slider_gain:t,gain:n}),a.postSimulation()},a.handleChange=function(e){return function(t){a.setState(Object(y.a)({},e,t.target.checked)),a.postSimulation()}},a.state={error:null,isLoaded:!1,updated:!1,on:0,gain:0,speed:0,power_bias:0,slider_gain:0,slider_speed:0,slider_power_bias:0,checkedSimulator:0},a.url="http://192.168.1.126:8079/api/simulation",a.can_update=!0,a.gain_scale=1,a.speed_scale=10,a.power_bias_scale=.5,a}return Object(u.a)(t,e),Object(o.a)(t,[{key:"setSimulationState",value:function(e){this.setState({isLoaded:!0,updated:!0,on:e.on,gain:e.gain,speed:e.speed,power_bias:e.power_bias,checkedSimulator:e.on,slider_gain:Math.round(e.gain*this.gain_scale),slider_speed:Math.round(e.speed*this.speed_scale),slider_power_bias:Math.round(e.power_bias*this.power_bias_scale/10)})}},{key:"getSimulation",value:function(){var e=this;fetch(this.url).then(function(e){return e.json()}).then(function(t){e.setSimulationState(t)},function(t){e.setState({isLoaded:!0,updated:!1,error:t})})}},{key:"postSimulation",value:function(){var e=this;this.can_update&&(this.can_update=!1,setTimeout(function(){var t=0;e.state.checkedSimulator&&(t=2),fetch(e.url,{method:"post",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({on:t,gain:e.state.gain,speed:e.state.speed,power_bias:e.state.power_bias})}).then(function(e){return e.json()}).then(function(t){e.setSimulationState(t),e.can_update=!0})},1e3))}},{key:"componentDidMount",value:function(){this.getSimulation()}},{key:"render",value:function(){var e=this.state,t=e.slider_speed,a=e.slider_gain,n=e.slider_power_bias,r=l.a.createElement(O.a,{row:!0},l.a.createElement(x.a,{control:l.a.createElement(T.a,{checked:this.state.checkedSimulator,onChange:this.handleChange("checkedSimulator"),value:"checkedSimulator",color:"primary"}),label:"Simulator On"}));return this.state.updated?this.state.on?l.a.createElement("div",null,l.a.createElement("br",null),l.a.createElement("br",null),r,l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Speed: ",(t/this.speed_scale).toFixed(1)," kts"),l.a.createElement(m.a,{value:t,"aria-labelledby":"set speed",onChange:this.handleSpeedSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Gain: ",Math.round(a/this.gain_scale)),l.a.createElement(m.a,{value:a,"aria-labelledby":"set kd",onChange:this.handleGainSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Applied force: ",(n/this.power_bias_scale).toFixed(0),"% max drive"),l.a.createElement(m.a,{value:n+50,"aria-labelledby":"set power bias",onChange:this.handlePowerBiasSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null)):l.a.createElement("div",null,l.a.createElement("br",null),l.a.createElement("br",null),r,l.a.createElement("br",null),l.a.createElement("br",null)):l.a.createElement("paper",null,l.a.createElement("h2",null,"No Communication: ",this.url))}}]),t}(n.Component),A=a(85),K=a.n(A),L=a(84),R=a.n(L),G=a(86),B=a.n(G),D=a(37),F=a.n(D),I=a(46),P=a.n(I),J=a(83),z=a.n(J),V=a(24),U=a.n(V),H=a(47);function W(e){return l.a.createElement(P.a,{component:"div",style:{padding:24}},e.children)}var q=function(e){function t(e){var a;return Object(s.a)(this,t),(a=Object(c.a)(this,Object(d.a)(t).call(this,e))).handleChange=function(e,t){a.setState({value:t})},a.state={value:0},a}return Object(u.a)(t,e),Object(o.a)(t,[{key:"render",value:function(){var e=this.props.classes,t=this.state.value;return l.a.createElement("div",null,l.a.createElement(z.a,null),l.a.createElement(R.a,{position:"static"},l.a.createElement(K.a,null,"Navigation Dashboard  NavDash v0.5"),l.a.createElement(B.a,{value:t,onChange:this.handleChange},l.a.createElement(F.a,{label:"Dash Board"}),l.a.createElement(F.a,{label:"Auto-helm Set Up"}),l.a.createElement(F.a,{label:"Auto-helm Simulator"}))),0===t&&l.a.createElement(W,null,l.a.createElement(U.a,{container:!0,className:e.root,spacing:24},l.a.createElement(U.a,{item:!0},l.a.createElement(S.a,{className:e.course},l.a.createElement(C,null))))),1===t&&l.a.createElement(W,null,l.a.createElement(U.a,{container:!0,className:e.root,spacing:24},l.a.createElement(U.a,{item:!0},l.a.createElement(S.a,{className:e.course},l.a.createElement(C,null))),l.a.createElement(U.a,{item:!0},l.a.createElement(S.a,{className:e.paper},l.a.createElement("h2",null,"Configuration"),l.a.createElement(k,null))),l.a.createElement(U.a,{item:!0},l.a.createElement(S.a,{className:e.paper},l.a.createElement("h2",null,"Simulation"),l.a.createElement(N,null))))),2===t&&l.a.createElement(W,null,l.a.createElement(N,null)))}}]),t}(n.Component),Q=Object(H.withStyles)(function(e){return{root:{flexGrow:1,backgroundColor:e.palette.background.paper},course:{padding:2*e.spacing.unit,textAlign:"center",color:e.palette.text.secondary,height:680,width:410},paper:{padding:2*e.spacing.unit,textAlign:"center",color:e.palette.text.secondary}}})(q);a(208);i.a.render(l.a.createElement(Q,null),document.getElementById("root"))},73:function(e,t,a){e.exports=a.p+"static/media/compass_rose.4794f22a.svg"},88:function(e,t,a){e.exports=a(209)},93:function(e,t,a){}},[[88,1,2]]]);
//# sourceMappingURL=main.87577557.chunk.js.map