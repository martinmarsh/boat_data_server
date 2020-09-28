(this.webpackJsonpnavdash=this.webpackJsonpnavdash||[]).push([[0],{206:function(e,t,a){},207:function(e,t,a){"use strict";a.r(t);var n=a(0),l=a.n(n),r=a(26),i=a.n(r),s=a(16),o=a(17),c=a(19),u=a(18),h=(a(91),a(92),a(20)),d=a.n(h),m=a(72),p=a.n(m),f=a(85),g=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(s.a)(this,a),(n=t.call(this,e)).state={error:null,rose:0},n.displayed={rose:-1,hts:-1,heading:-1},n}return Object(o.a)(a,[{key:"updateSVGCompass",value:function(){var e=this.props,t=e.heading,a=e.hts,n=this.state.rose;if(t!==this.displayed.heading){var l=document.getElementById("compass_heading");l&&(console.log(l),l.setAttribute("transform","rotate("+t+",600,600)"),this.displayed.heading=t)}if(a!==this.displayed.hts){var r=document.getElementById("compass_course");r&&(console.log(r),r.setAttribute("transform","rotate("+a+",600,600)"))}if(n!==this.displayed.rose){var i=document.getElementById("compass_rose");i&&(console.log(i),i.setAttribute("transform","rotate("+n+",600,600)"),this.displayed.rose=n)}}},{key:"render",value:function(){return this.updateSVGCompass(),l.a.createElement("div",{className:"App-Compass"},l.a.createElement(f.a,{src:p.a}))}}]),a}(n.Component),E=a(21),_=a.n(E),v=a(15),b=a.n(v),C=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(s.a)(this,a),(n=t.call(this,e)).handleHTSSliderChange=function(e,t){n.setState({hts_slider_value:t}),n.conditionSetHTS(3.6*(t-50)),n.postHts()},n.handleTrimSliderChange=function(e,t){n.setState({trim_slider_value:t});var a=(t-50)/10+n.state.hts_slider_value-50;n.conditionSetHTS(3.6*a),n.postHts()},n.state={error:null,isLoaded:!1,updated:!1,hts:0,heading:0,rose:0,rudder:0,power:0,pitch:0,roll:0,auto_helm:0,auto_mode:0,hts_slider_value:50,trim_slider_value:50},console.log("configuration:"+V),n.end_point="/api/orientation",n.set_hts=0,n.local_control=0,n.local_control_count_down=3,n}return Object(o.a)(a,[{key:"getCompass",value:function(){var e=this;console.log("configuration:"+V),""!==V&&(void 0===this.url&&(this.url=V+this.end_point),fetch(this.url).then((function(e){return e.json()})).then((function(t){e.setState({isLoaded:!0,updated:!0,hts:t.hts,heading:t.heading,pitch:t.pitch,roll:t.roll,rudder:t.rudder,power:t.power,calibration:t.calibration,auto_helm:t.auto_helm})}),(function(t){e.setState({isLoaded:!0,updated:!1,error:t})})))}},{key:"postHts",value:function(){var e=this;fetch(this.url,{method:"post",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({hts:this.set_hts,auto_mode:this.state.auto_mode})}).then((function(e){return e.json()})).then((function(t){e.local_control=e.local_control_count_down,e.setState({isLoaded:!0,updated:!0,hts:t.hts,heading:t.heading})}))}},{key:"componentDidMount",value:function(){var e=this;this.getCompass(),this.timer=setInterval((function(){e.getCompass(),e.set_hts!==e.state.hts&&(e.local_control>0?e.local_control--:e.setHTS(e.state.hts))}),333)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"conditionSetHTS",value:function(e){e<0&&(e=360+e),e>360&&(e-=360),this.set_hts=Math.round(e)}},{key:"setHTS",value:function(e){this.conditionSetHTS(e);var t=Math.round(this.set_hts/3.6+50);t<0&&(t=100+t),t>100&&(t-=100),this.setState({hts_slider_value:t})}},{key:"setAutoMode",value:function(e){var t=2;1===e&&(t=1),this.state.auto_mode=t}},{key:"render",value:function(){var e=this,t=this.state,a=t.hts_slider_value,n=t.hts,r=t.trim_slider_value,i=t.calibration,s=t.rudder,o=t.power,c=t.pitch,u=t.roll,h=t.auto_helm,m=this.state.heading;m=Math.round(m);var p=180,f=180*Math.abs(o/1e6),E=178+s/30*178,v="green";o<0&&(v="red",p=180-f);var C="red",S="OFF - Press to turn on";1===h&&(C="green",S="ON  - Press to turn off ");var y,k=i,j=3&k,H=3&(k>>>=2),T=3&(k>>>=2),N=3&(k>>>=2),O={color:"white",backgroundColor:C,padding:"10px",fontFamily:"Arial"};return y=this.state.updated?l.a.createElement(g,{hts:this.set_hts,heading:this.state.heading}):l.a.createElement(b.a,null,l.a.createElement("h2",null,"No Communication: ",this.url)),l.a.createElement("div",null,l.a.createElement("div",{className:"floatLeft"},i,": s",N," g",T," a",H," c",j),l.a.createElement("h4",null,"Roll ",l.a.createElement("b",null,u),"  \xa0\xa0 \xa0Pitch ",l.a.createElement("b",null,c)),l.a.createElement("div",{className:"pad"},y),l.a.createElement("div",{className:"pad"},l.a.createElement("svg",{width:"410",height:"8"},l.a.createElement("rect",{x:p,y:"4",width:f,height:"2",fill:v}),l.a.createElement("rect",{x:E,width:"4",height:"8",fill:"blue"}),l.a.createElement("rect",{x:"179",width:"2",height:"8",fill:"black"}),l.a.createElement("rect",{x:"0",width:"2",height:"8",fill:"black"}),l.a.createElement("rect",{x:"360",width:"2",height:"8",fill:"black"})),l.a.createElement("h3",null,"Heading ",l.a.createElement("b",null,m)," M \xa0\xa0 \xa0HTS ",l.a.createElement("b",null,n)," M"),l.a.createElement("h4",null,"Course to Steer: "),l.a.createElement("div",null,l.a.createElement("span",{className:"floatLeft"},l.a.createElement(_.a,{color:"primary",onClick:function(){e.setHTS(e.set_hts-85),e.postHts()}},"-85"),l.a.createElement(_.a,{color:"primary",onClick:function(){e.setHTS(e.set_hts-5),e.postHts()}},"-5")),l.a.createElement("span",{className:"floatRight"},l.a.createElement(_.a,{color:"primary",onClick:function(){e.setHTS(e.set_hts+5),e.postHts()}},"+5"),l.a.createElement(_.a,{color:"primary",onClick:function(){e.setHTS(e.set_hts+85),e.postHts()}},"+85")),l.a.createElement(d.a,{value:a,"aria-labelledby":"set hts",onChange:this.handleHTSSliderChange})),l.a.createElement("br",null)," ",l.a.createElement("br",null),l.a.createElement("h4",null,"Trim Course:"),l.a.createElement(d.a,{value:r,"aria-labelledby":"trim course",onChange:this.handleTrimSliderChange}),l.a.createElement("br",null),l.a.createElement(_.a,{size:"small",color:"primary",onClick:function(){e.local_control=e.local_control_count_down;var t=.36*(r-50);e.setHTS(e.set_hts-t),e.setState({trim_slider_value:50})}},"Keep"),l.a.createElement(_.a,{size:"small",color:"primary",onClick:function(){e.conditionSetHTS(3.6*(a-50)),e.postHts(),e.setState({trim_slider_value:50})}},"Return"),l.a.createElement("div",{className:"floatRight",style:O,onClick:function(){e.setAutoMode(h),e.postHts()}},S)))}}]),a}(n.Component),S=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(s.a)(this,a),(n=t.call(this,e)).handleCalibrationButton=function(e,t){n.setState({set_cal:t}),n.postCalibration()},n.handleTsfSliderChange=function(e,t){n.setState({slider_tsf:Math.round(t)}),n.postCalibration()},n.handleGainSliderChange=function(e,t){n.setState({slider_gain:Math.round(t)}),n.postCalibration()},n.state={error:null,isLoaded:!1,updated:!1,tsf:0,gain:0,set_cal:0,slider_tsf:0,slider_gain:0,gain_slider_multiplier:6400,tsf_slider_multiplier:1.5},n.end_point="/api/calibration",n.can_update=!0,n}return Object(o.a)(a,[{key:"setCalibrationState",value:function(e){var t=e.gain,a=e.tsf;this.setState({isLoaded:!0,updated:!0,gain:t,tsf:a,slider_gain:Math.round(t/this.state.gain_slider_multiplier),slider_tsf:Math.round(a/this.state.tsf_slider_multiplier),set_cal:e.set_cal,calibration:e.calibration})}},{key:"getCalibration",value:function(){var e=this;""!==V&&(void 0===this.url&&(this.url=V+this.end_point),fetch(this.url).then((function(e){return e.json()})).then((function(t){e.setCalibrationState(t)}),(function(t){e.setState({isLoaded:!0,updated:!1,error:t})})))}},{key:"postCalibration",value:function(){var e=this;this.can_update&&(this.can_update=!1,setTimeout((function(){fetch(e.url,{method:"post",headers:{Accept:"application/json, text/plain, */*","Content-Type":"application/json"},body:JSON.stringify({gain:Math.round(e.state.slider_gain*e.state.gain_slider_multiplier),tsf:Math.round(e.state.slider_tsf*e.state.tsf_slider_multiplier),set_cal:e.state.set_cal})}).then((function(e){return e.json()})).then((function(t){e.setCalibrationState(t),e.can_update=!0}))}),1e3))}},{key:"componentDidMount",value:function(){var e=this;this.getCalibration(),this.timer=setInterval((function(){e.getCalibration()}),5e3)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"render",value:function(){var e=this,t=this.state,a=t.slider_tsf,n=t.slider_gain;return this.state.updated?l.a.createElement("div",null,l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Gain: ",n,"%"),l.a.createElement(d.a,{value:n,"aria-labelledby":"set gain",onChange:this.handleGainSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("h3",null,"Reduce Desired Turn Rate (tsf): ",a,"%"),l.a.createElement(d.a,{value:a,"aria-labelledby":"set tsf",onChange:this.handleTsfSliderChange}),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement(b.a,{className:"pad"},l.a.createElement("h3",null,"Compass/Orientation Chip Calibration:"),l.a.createElement(_.a,{variant:"contained",size:"small",color:"primary",onClick:function(t){e.handleCalibrationButton(t,1)}},"Erase"),"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0",l.a.createElement(_.a,{variant:"contained",size:"small",color:"primary",onClick:function(t){e.handleCalibrationButton(t,2)}},"Store"),l.a.createElement("br",null),l.a.createElement("br",null),l.a.createElement("br",null))):l.a.createElement(b.a,null,l.a.createElement("h2",null,"No Communication: ",this.url))}}]),a}(n.Component),y=a(78),k=a.n(y),j=a(79),H=a.n(j),T=a(80),N=a.n(T),O=(n.Component,a(83)),w=a.n(O),M=a(82),x=a.n(M),A=a(84),L=a.n(A),I=a(36),B=a.n(I),G=a(45),R=a.n(G),D=a(81),z=a.n(D),J=a(23),F=a.n(J),P=a(46);function U(e){return l.a.createElement(R.a,{component:"div",style:{padding:24}},e.children)}var V="",W=function(e){Object(c.a)(a,e);var t=Object(u.a)(a);function a(e){var n;return Object(s.a)(this,a),(n=t.call(this,e)).handleChange=function(e,t){n.setState({value:t})},n.state={value:0},fetch("/config.json").then((function(e){return e.json()})).then((function(e){console.log("read config:"+e.host),V=e.host})),n}return Object(o.a)(a,[{key:"render",value:function(){var e=this.props.classes,t=this.state.value;return l.a.createElement("div",null,l.a.createElement(z.a,null),l.a.createElement(x.a,{position:"static"},l.a.createElement(w.a,null,"Navigation Dashboard  NavDash v0.7"),l.a.createElement(L.a,{value:t,onChange:this.handleChange},l.a.createElement(B.a,{label:"Heading"}),l.a.createElement(B.a,{label:"Steering"}),l.a.createElement(B.a,{label:"Auto-helm Set Up"}))),0===t&&l.a.createElement(U,null,l.a.createElement(F.a,{container:!0,className:e.root,spacing:24},l.a.createElement(F.a,{item:!0},l.a.createElement(b.a,{className:e.course},l.a.createElement(C,null))))),1===t&&l.a.createElement(U,null,l.a.createElement(F.a,{container:!0,className:e.root,spacing:24},l.a.createElement(F.a,{item:!0},l.a.createElement(b.a,{className:e.course},l.a.createElement(C,null))),l.a.createElement(F.a,{item:!0},l.a.createElement(b.a,{className:e.paper},l.a.createElement("h2",null,"Steering"))))),2===t&&l.a.createElement(U,null,l.a.createElement(F.a,{container:!0,className:e.root,spacing:24},l.a.createElement(F.a,{item:!0},l.a.createElement(b.a,{className:e.course},l.a.createElement(C,null))),l.a.createElement(F.a,{item:!0},l.a.createElement(b.a,{className:e.paper},l.a.createElement("h2",null,"Configuration"),l.a.createElement(S,null))))))}}]),a}(n.Component),K=Object(P.withStyles)((function(e){return{root:{flexGrow:1,backgroundColor:e.palette.background.paper},course:{padding:2*e.spacing.unit,textAlign:"center",color:e.palette.text.secondary,height:680,width:410},paper:{padding:2*e.spacing.unit,textAlign:"center",color:e.palette.text.secondary}}}))(W);a(206);i.a.render(l.a.createElement(K,null),document.getElementById("root"))},72:function(e,t,a){e.exports=a.p+"static/media/compass_rose.4794f22a.svg"},86:function(e,t,a){e.exports=a(207)},91:function(e,t,a){}},[[86,1,2]]]);
//# sourceMappingURL=main.dfa29909.chunk.js.map