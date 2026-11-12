import { Routes, Route } from "react-router-dom";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import Login from "./components/Login/Login";
import PostReview from "./components/Dealers/PostReview";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;
