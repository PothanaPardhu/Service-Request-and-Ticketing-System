import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { LayoutDashboard, Ticket, Clock, CheckCircle2, AlertCircle, Plus, LogOut, Settings2 } from 'lucide-react';
import { motion } from 'framer-motion';
import TicketModal from '../components/TicketModal';
import ActionModal from '../components/ActionModal';

const Dashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isTicketModalOpen, setIsTicketModalOpen] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [isActionModalOpen, setIsActionModalOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const ticketsRes = await client.get('/tickets/');
      setTickets(ticketsRes.data.results || ticketsRes.data);
    } catch (err) {
      console.error('Tickets fetch error:', err);
    }

    try {
      const statsRes = await client.get('/analytics/');
      setStats(statsRes.data);
    } catch (err) {
      console.warn('Analytics access denied (Admin only)');
      setStats(null);
    }
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    window.location.href = '/login';
  };

  const handleManage = (ticket) => {
    setSelectedTicket(ticket);
    setIsActionModalOpen(true);
  };

  if (loading) return <div style={{ color: 'white', textAlign: 'center', marginTop: '10rem' }}>Initializing System...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Service Dashboard</h1>
          <p style={{ color: 'var(--text-dim)' }}>Welcome back to the command center</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={() => setIsTicketModalOpen(true)} className="btn btn-primary">
            <Plus size={20} />
            New Request
          </button>
          <button onClick={handleLogout} className="btn" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>
            <LogOut size={20} />
          </button>
        </div>
      </header>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
        <StatCard icon={<Ticket color="#6366f1" />} label="Total Tickets" value={stats?.total_tickets || '—'} />
        <StatCard icon={<Clock color="#fbbf24" />} label="Avg Resolution" value={stats?.avg_resolution_hours ? `${stats.avg_resolution_hours}h` : '—'} />
        <StatCard icon={<AlertCircle color="#ef4444" />} label="SLA Breaches" value={stats?.overdue_count ?? '—'} />
        <StatCard icon={<CheckCircle2 color="#10b981" />} label="Success Rate" value="98.2%" />
      </div>

      {/* Ticket List */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="glass" 
        style={{ padding: '1.5rem', borderRadius: '20px' }}
      >
        <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Recent Activity</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--glass-border)', color: 'var(--text-dim)' }}>
                <th style={{ padding: '1rem' }}>ID</th>
                <th style={{ padding: '1rem' }}>Ticket Title</th>
                <th style={{ padding: '1rem' }}>Status</th>
                <th style={{ padding: '1rem' }}>Priority</th>
                <th style={{ padding: '1rem' }}>Agent</th>
                <th style={{ padding: '1rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((ticket) => (
                <tr key={ticket.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', transition: 'background 0.2s' }}>
                  <td style={{ padding: '1.25rem' }}>#{ticket.id}</td>
                  <td style={{ padding: '1.25rem', fontWeight: 500 }}>{ticket.title}</td>
                  <td style={{ padding: '1.25rem' }}>
                    <span className={`status-badge status-${ticket.status.toLowerCase()}`}>
                      {ticket.status}
                    </span>
                  </td>
                  <td style={{ padding: '1.25rem' }}>
                    <span style={{ color: getPriorityColor(ticket.priority), fontWeight: 600 }}>{ticket.priority}</span>
                  </td>
                  <td style={{ padding: '1.25rem', color: 'var(--text-dim)' }}>
                    {ticket.assigned_to?.email || 'Unassigned'}
                  </td>
                  <td style={{ padding: '1.25rem' }}>
                    <button onClick={() => handleManage(ticket)} className="btn" style={{ padding: '0.4rem', borderRadius: '8px', background: 'rgba(255,255,255,0.05)' }}>
                      <Settings2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Modals */}
      <TicketModal 
        isOpen={isTicketModalOpen} 
        onClose={() => setIsTicketModalOpen(false)} 
        onRefresh={fetchData}
      />
      
      <ActionModal 
        isOpen={isActionModalOpen}
        onClose={() => setIsActionModalOpen(false)}
        ticket={selectedTicket}
        onRefresh={fetchData}
      />
    </div>
  );
};

const StatCard = ({ icon, label, value }) => (
  <div className="glass" style={{ padding: '1.5rem', borderRadius: '16px', display: 'flex', alignItems: 'center', gap: '1rem' }}>
    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px' }}>
      {icon}
    </div>
    <div>
      <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>{label}</p>
      <p style={{ fontSize: '1.5rem', fontWeight: 700 }}>{value}</p>
    </div>
  </div>
);

const getPriorityColor = (p) => {
  switch(p) {
    case 'CRITICAL': return '#ef4444';
    case 'HIGH': return '#f97316';
    case 'MEDIUM': return '#fbbf24';
    default: return '#94a3b8';
  }
};

export default Dashboard;
