import React, { useState } from 'react'
import { createCustomer } from '../api/customers'

export default function CustomerForm({ onSaved }: { onSaved?: (c:any)=>void }){
  const [legal_name, setLegalName] = useState('')
  const [external_reference, setExternalReference] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  async function submit(e: React.FormEvent){
    e.preventDefault()
    try{
      const payload = { legal_name, external_reference }
      const saved = await createCustomer(payload)
      setMsg('Created')
      setLegalName('')
      setExternalReference('')
      onSaved && onSaved(saved)
    }catch(err:any){
      setMsg(err?.message || 'Create failed')
    }
  }

  return (
    <form onSubmit={submit} style={{marginTop:10}}>
      <div>
        <label>Legal name</label>
        <input value={legal_name} onChange={e=>setLegalName(e.target.value)} />
      </div>
      <div>
        <label>External reference</label>
        <input value={external_reference} onChange={e=>setExternalReference(e.target.value)} />
      </div>
      <div>
        <button className="button" type="submit">Create Customer</button>
      </div>
      {msg && <div style={{marginTop:10}}>{msg}</div>}
    </form>
  )
}
