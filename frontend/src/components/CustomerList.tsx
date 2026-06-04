import React from 'react'

export default function CustomerList({
  items,
  onEdit,
  onDelete,
}: {
  items: any[]
  onEdit: (item:any)=>void
  onDelete: (id:string)=>void
}){
  if(items.length === 0){
    return <p>No customers yet.</p>
  }

  return (
    <table style={{width:'100%', marginTop: 16, borderCollapse:'collapse'}}>
      <thead>
        <tr>
          <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Legal Name</th>
          <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Reference</th>
          <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Actions</th>
        </tr>
      </thead>
      <tbody>
        {items.map(item => (
          <tr key={item.id}>
            <td style={{padding:'8px 0'}}>{item.legal_name}</td>
            <td style={{padding:'8px 0'}}>{item.external_reference}</td>
            <td style={{padding:'8px 0'}}>
              <button className="button" onClick={() => onEdit(item)} style={{marginRight: 8}}>
                Edit
              </button>
              <button className="button" onClick={() => onDelete(item.id)}>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
