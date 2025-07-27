// Frontend: Modern ChatGPT-style Interface
import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { SendHorizonal } from "lucide-react";
import axios from "axios";

export default function ScholarshipChat() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi! Ask me anything about scholarships." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/ask", { question: input });
      const botMsg = { role: "bot", text: res.data.answer };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Oops! Something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 p-4 flex flex-col items-center">
      <h1 className="text-3xl font-bold text-purple-700 mb-4">Scholarship Q&A Assistant</h1>
      <Card className="w-full max-w-2xl bg-white shadow-xl rounded-2xl flex flex-col overflow-hidden">
        <CardContent className="flex-1 space-y-2 p-4 overflow-y-auto h-[60vh]">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={\`rounded-xl p-3 text-sm whitespace-pre-wrap \${msg.role === "bot" ? "bg-purple-100 text-left text-gray-800" : "bg-blue-100 text-right text-blue-800 ml-auto"}\`}
            >
              {msg.text}
            </div>
          ))}
        </CardContent>
        <div className="flex items-center border-t p-4 gap-2">
          <Input
            className="flex-1"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question..."
          />
          <Button onClick={sendMessage} disabled={loading}>
            <SendHorizonal className="h-4 w-4" />
          </Button>
        </div>
      </Card>
    </div>
  );
}
