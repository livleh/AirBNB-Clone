import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Property from './pages/property';

function App() {
  return <BrowserRouter>
      <Routes>
        <Route path="/">
        <Route index element={<Property />} />
        {/* <Route path="groups" element={<Groups />} />
        <Route path="marketplace" element={<Marketplace />} />
        <Route path="watch" element={<Watch />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>;
}

export default App;
