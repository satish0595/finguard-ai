import { request } from './client'

export type DashboardSummary = {
  customers_total: number
  customers_high_risk: number
  customers_pending_review: number
  transactions_total: number
  transactions_pending: number
  open_alerts: number
  critical_alerts: number
  open_cases: number
  urgent_cases: number
}

export async function getDashboardSummary() {
  return await request('/dashboard/summary') as DashboardSummary
}