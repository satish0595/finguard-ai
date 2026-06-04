import React, { useEffect, useState } from 'react'
import { createCustomer, updateCustomer } from '../api/customers'

export default function CustomerForm({
  customer,
  onSaved,
  onCancel,
}: {
  customer?: any
  onSaved?: (c:any)=>void
  onCancel?: ()=>void
}){
  const [legal_name, setLegalName] = useState('')
  const [external_reference, setExternalReference] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  useEffect(() => {
    if (customer) {
      setLegalName(customer.legal_name || '')
      setExternalReference(customer.external_reference || '')
    } else {
      setLegalName('')
      setExternalReference('')
    }
  }, [customer])

  async function submit(e: React.FormEvent){
    e.preventDefault()
    try{
      const payload = { legal_name, external_reference }
      const saved = customer
        ? await updateCustomer(customer.id, payload)
        : await createCustomer(payload)
      setMsg(customer ? 'Updated' : 'Created')
      if (!customer) {
        setLegalName('')
        setExternalReference('')
      }
      onSaved && onSaved(saved)
    }catch(err:any){
      setMsg(err?.message || (customer ? 'Update failed' : 'Create failed'))
    }
  }

  return (
    <form onSubmit={submit} style={{marginTop:10, border:'1px solid #ddd', padding:16, borderRadius:6}}>
      <h3>{customer ? 'Edit Customer' : 'New Customer'}</h3>
      <div>
        <label>Legal name</label>
        <input value={legal_name} onChange={e=>setLegalName(e.target.value)} />
      </div>
      <div>
        <label>External reference</label>
        <input value={external_reference} onChange={e=>setExternalReference(e.target.value)} />
      </div>
      <div>
        <button className="button" type="submit">{customer ? 'Save Changes' : 'Create Customer'}</button>
        {customer && onCancel && (
          <button type="button" className="button" style={{marginLeft:8}} onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
      {msg && <div style={{marginTop:10}}>{msg}</div>}
    </form>
  )
}
