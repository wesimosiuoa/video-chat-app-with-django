// const AgoraRTC_N4221 = require("../assets/AgoraRTC_N-4.22.1")

const APP_ID = '4fcd24e9e7c741c9902a5ac0a9313947'
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))
let NAME = sessionStorage.getItem('name')

console.log (' Streams.js connected ')

const client = AgoraRTC.createClient ({ mode : 'rtc', codec: 'vp8'})

let localTracks = []
let remoteUsers = {}
let joinAndDisplayLocalStream = async () => {
    try {
        document.getElementById('room-name').innerText = CHANNEL

        client.on('user-published', handleUserJoined)
        client.on('user-left', handleuserLeft)


        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)

        // Create microphone and camera tracks
        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
        
        let member = await createMember ()
        

        let player = `<div class="col-lg-6 col-md-8 col-sm-12 video-container card p-3 shadow-sm" id="user-container-${UID}">
            <div class="username-wrapper mb-2 text-center">
                <span class="user-name h5">${member.name}</span>
            </div>
            <div class="video-player bg-dark" id="user-${UID}" style="height: 400px; width: 100%;"></div>
        </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

        localTracks[1].play(`user-${UID}`)
        await client.publish([localTracks[0], localTracks[1]])
    } catch (error) {
        console.error("Error creating microphone and camera tracks: ", error)
    }
}
let handleUserJoined = async (user, mediaType) => {
    try{
        remoteUsers[user.uid] = user
        await client.subscribe (user, mediaType)
        

        if (mediaType === 'video'){
            let player = document.getElementById(`user-container-${user.uid}`)

            if (player != null){
                player.remove()
            }


            let member = await getMember(user)
            player = `<div class="col-lg-6 col-md-8 col-sm-12 video-container card p-3 shadow-sm" id="user-container-${user.uid}">
                    <div class="username-wrapper mb-2 text-center">
                        <span class="user-name h5">${member.name}</span>
                    </div>
                    <div class="video-player bg-dark" id="user-${user.uid}" style="height: 400px; width: 100%;"></div>
                </div>`

            document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
            user.videoTrack.play(`user-${user.uid}`)
        }

        if (mediaType === 'audio'){
            user.audioTrack.play()
        }
    }
    catch (error){
        console.error (" Error in handling user joined ", error )
    }
}

let handleuserLeft = async (user) => {
    delete remoteUsers [user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    const indexUrl = "{% url 'home' %}";
    for ( let i = 0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()

    window.addEventListener('beforeunload', () => deleteMember());
    console.log(' URL : ' , indexUrl)
    window.open ('/index', '_self')   
}
let toggleCamera = async (e) => {
    if (localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style=backgroundColor = '#fff'
    }
    else {
        await localTracks[1].setMuted(true)
        e.target.style=backgroundColor = 'red'
    }
}
let toggleMic = async (e) => {
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style=backgroundColor = '#fff'
    }
    else {
        await localTracks[0].setMuted(true)
        e.target.style=backgroundColor = 'red'
    }
}
joinAndDisplayLocalStream()


let createMember = async () => {
    let response = await fetch('/create_member/', 
        {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            }, 
            body: JSON.stringify({'name':NAME, 'room_name': CHANNEL, 'UID': UID})
        }
    )
    let member = await response.json()
    return member

}

let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member

}

let deleteMember = async () => {
    let response = await fetch('/delete_member/', 
        {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            }, 
            body: JSON.stringify({'name':NAME, 'room_name': CHANNEL, 'uid': uid})
        }
    )
    let member = await response.json()
   

}

window.addEventListener('beforeunload', deleteMember())
document.getElementById ('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById ('camera-btn').addEventListener('click', toggleCamera)
document.getElementById ('mic-btn').addEventListener('click', toggleMic)