import { useState } from "react";

export default function Property() {
  const [foo, setFoo] = useState({})
  const [loading, setLoading] = useState(true);
  fetch('http://localhost:8000/property/', {
    headers: { 'Authorization': 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMzUzMzIzLCJpYXQiOjE2ODEzNTE1MjMsImp0aSI6ImI3YmY1NzViNTJiZTRiMTQ5MzBhMDI4ZDViZjkxNjQ2IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhIn0.v60fDAgK9HRCn0wjfGRPbp4ztUotP6Nbkd5kOcujMiU' } 
  })
  .then(response => response.json())
  .then(json => {setFoo(JSON.stringify(json));
  setLoading(false)})

  if (loading) {
    return <>
      Loading...
    </>
  }
  return <>
    { foo }
        </>
}