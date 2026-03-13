import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import {
  FaUserMd,
  FaClock,
  FaCalendar,
  FaComments,
  FaSmile,
  FaRobot,
  FaPaperPlane
} from "react-icons/fa";

function App() {

  const API = "http://127.0.0.1:8000";

  const [text,setText] = useState("");
  const [messages,setMessages] = useState([]);

  const [hcpName,setHcpName] = useState("");
  const [interactionType,setInteractionType] = useState("");
  const [topics,setTopics] = useState("");
  const [sentiment,setSentiment] = useState("");
  const [followUp,setFollowUp] = useState("");
  const [date,setDate] = useState("");
  const [time,setTime] = useState("");

  const [loading,setLoading] = useState(false);
  const [interactionId,setInteractionId] = useState(null);


  const submitInteraction = async () => {

    if(!text.trim()) return;

    const userMsg = {role:"user",content:text};
    setMessages(prev => [...prev,userMsg]);

    try{

      setLoading(true);

      const response = await axios.post(`${API}/process`,{text});
      const data = response.data;

      if(data.id) setInteractionId(data.id);

      setHcpName(data.doctor_name || "");
      setDate(data.date || "");
      setTime(data.time || "");
      setInteractionType(data.interaction_type || "");
      setTopics(data.topics || "");
      setSentiment(data.sentiment || "");
      setFollowUp(data.followup || "");

      const aiMsg = {
        role:"assistant",
        content:`Interaction processed ✓ Doctor: ${data.doctor_name}`
      };

      setMessages(prev => [...prev,aiMsg]);

    }
    catch(error){

      alert("Backend connection failed");

    }
    finally{

      setLoading(false);

    }

    setText("");

  };


  useEffect(()=>{

    if(!interactionId) return;

    axios.put(`${API}/update/${interactionId}`,{

      doctor_name:hcpName,
      date:date,
      time:time,
      interaction_type:interactionType,
      topics:topics,
      sentiment:sentiment,
      followup:followUp

    });

  },[hcpName,date,time,interactionType,topics,sentiment,followUp,interactionId]);


  return (

    <div className="app">

      <div className="header">

        <div className="brand">

          <div className="logo">
            <FaRobot/>
          </div>

          <h1>AI CRM HCP Interaction Logger</h1>

        </div>

      </div>


      <div className="mainLayout">

        {/* LEFT PANEL */}

        <div className="formPanel">

          <h2>Log HCP Interaction</h2>

          <div className="field">
            <label><FaUserMd/> HCP Name</label>
            <input value={hcpName} onChange={(e)=>setHcpName(e.target.value)} />
          </div>

          <div className="formGrid">

            <div className="field">
              <label><FaCalendar/> Date</label>
              <input type="date" value={date} onChange={(e)=>setDate(e.target.value)} />
            </div>

            <div className="field">
              <label><FaClock/> Time</label>
              <input type="time" value={time} onChange={(e)=>setTime(e.target.value)} />
            </div>

          </div>

          <div className="field">
            <label>Interaction Type</label>
            <select value={interactionType} onChange={(e)=>setInteractionType(e.target.value)}>
              <option value="">Select</option>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Discussion">Discussion</option>
            </select>
          </div>

          <div className="field">
            <label><FaComments/> Topics Discussed</label>
            <textarea value={topics} onChange={(e)=>setTopics(e.target.value)} />
          </div>

          <div className="field">

            <label><FaSmile/> Sentiment</label>

            <div className="sentimentRow">

              <button className={sentiment==="Positive"?"active":""} onClick={()=>setSentiment("Positive")}>Positive</button>
              <button className={sentiment==="Neutral"?"active":""} onClick={()=>setSentiment("Neutral")}>Neutral</button>
              <button className={sentiment==="Negative"?"active":""} onClick={()=>setSentiment("Negative")}>Negative</button>

            </div>

          </div>

          <div className="field">
            <label>Follow-up Actions</label>
            <textarea value={followUp} onChange={(e)=>setFollowUp(e.target.value)} />
          </div>

        </div>


        {/* AI PANEL */}

        <div className="aiPanel">

          <h2><FaRobot/> AI Assistant</h2>

          <div className="chatWindow">

            {messages.map((msg,i)=>(
              <div key={i} className={msg.role==="user"?"chatUser":"chatAI"}>
                {msg.content}
              </div>
            ))}

            {loading && <div className="chatAI">AI analyzing...</div>}

          </div>

          <div className="chatInput">

            <textarea
              value={text}
              onChange={(e)=>setText(e.target.value)}
              placeholder="Describe interaction naturally..."
            />

            <button onClick={submitInteraction}>
              <FaPaperPlane/>
            </button>

          </div>

        </div>

      </div>

    </div>

  );

}

export default App;