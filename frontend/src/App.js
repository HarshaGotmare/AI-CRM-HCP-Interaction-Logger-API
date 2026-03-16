import { useState } from "react";
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

  const [text, setText] = useState("");
  const [messages, setMessages] = useState([]);

  const [hcpName, setHcpName] = useState("");
  const [interactionType, setInteractionType] = useState("");
  const [topics, setTopics] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

  const [loading, setLoading] = useState(false);
  const [interactionId, setInteractionId] = useState(null);

  const submitInteraction = async () => {
    if (!text.trim() || loading) return;

    const userText = text.trim();
    setMessages((prev) => [...prev, { role: "user", content: userText }]);

    try {
      setLoading(true);

      const response = await axios.post(`${API}/process`, { text: userText });
      const data = response.data;

      const nextDoctor = data.doctor_name ?? hcpName;
      const nextDate = data.date ?? date;
      const nextTime = data.time ?? time;
      const nextInteractionType = data.interaction_type ?? interactionType;
      const nextTopics = data.topics ?? topics;
      const nextSentiment = data.sentiment ?? sentiment;
      const nextFollowUp = data.followup ?? followUp;

      if (data.id) setInteractionId(data.id);

      setHcpName(nextDoctor || "");
      setDate(nextDate || "");
      setTime(nextTime || "");
      setInteractionType(nextInteractionType || "");
      setTopics(nextTopics || "");
      setSentiment(nextSentiment || "");
      setFollowUp(nextFollowUp || "");

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Interaction processed ✓ Doctor: ${nextDoctor || "Unknown"} | Date: ${nextDate || "No date"} | Time: ${nextTime || "No time"}`
        }
      ]);

      setText("");
    } catch (error) {
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    if (!interactionId) {
      alert("No interaction selected to update");
      return;
    }

    try {
      await axios.put(`${API}/update/${interactionId}`, {
        doctor_name: hcpName,
        date,
        time,
        interaction_type: interactionType,
        topics,
        sentiment,
        followup: followUp
      });
      alert("Interaction updated successfully");
    } catch (error) {
      alert("Update failed");
    }
  };

  return (
    <div className="app">
      <div className="header">
        <div className="brand">
          <div className="logo">
            <FaRobot />
          </div>
          <h1>AI CRM HCP Interaction Logger</h1>
        </div>
      </div>

      <div className="mainLayout">
        <div className="formPanel">
          <h2>Log HCP Interaction</h2>

          <div className="field">
            <label><FaUserMd /> HCP Name</label>
            <input value={hcpName} onChange={(e) => setHcpName(e.target.value)} />
          </div>

          <div className="formGrid">
            <div className="field">
              <label><FaCalendar /> Date</label>
              <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            </div>

            <div className="field">
              <label><FaClock /> Time</label>
              <input type="time" value={time} onChange={(e) => setTime(e.target.value)} />
            </div>
          </div>

          <div className="field">
            <label>Interaction Type</label>
            <select value={interactionType} onChange={(e) => setInteractionType(e.target.value)}>
              <option value="">Select</option>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Discussion">Discussion</option>
            </select>
          </div>

          <div className="field">
            <label><FaComments /> Topics Discussed</label>
            <textarea value={topics} onChange={(e) => setTopics(e.target.value)} />
          </div>

          <div className="field">
            <label><FaSmile /> Sentiment</label>
            <div className="sentimentRow">
              <button type="button" className={sentiment === "Positive" ? "active" : ""} onClick={() => setSentiment("Positive")}>
                Positive
              </button>
              <button type="button" className={sentiment === "Neutral" ? "active" : ""} onClick={() => setSentiment("Neutral")}>
                Neutral
              </button>
              <button type="button" className={sentiment === "Negative" ? "active" : ""} onClick={() => setSentiment("Negative")}>
                Negative
              </button>
            </div>
          </div>

          <div className="field">
            <label>Follow-up Actions</label>
            <textarea value={followUp} onChange={(e) => setFollowUp(e.target.value)} />
          </div>

          <button className="updateBtn" type="button" onClick={handleUpdate}>
            Update Interaction
          </button>
        </div>

        <div className="aiPanel">
          <h2><FaRobot /> AI Assistant</h2>

          <div className="chatWindow">
            {messages.map((msg, i) => (
              <div key={i} className={msg.role === "user" ? "chatUser" : "chatAI"}>
                {msg.content}
              </div>
            ))}
            {loading && <div className="chatAI">AI analyzing...</div>}
          </div>

          <div className="chatInput">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Describe interaction naturally..."
            />
            <button type="button" onClick={submitInteraction} disabled={loading}>
              <FaPaperPlane />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;