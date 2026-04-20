import React, { useState } from 'react';
import client from '../api/client';
import { X, CheckCircle, UserPlus, MessageSquare } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ActionModal = ({ isOpen, onClose, ticket, onRefresh }) => {
  const [status, setStatus] = useState(ticket?.status || '');
  const [loading, setLoading] = useState(false);

  const handleUpdateStatus = async () => {
    setLoading(true);
    try {
      await client.patch(`/tickets/${ticket.id}/status/`, { status });
      onRefresh();
      onClose();
    } catch (err) {
      alert(err.response?.data?.error || 'Update failed');
    } finally {
      setLoading(false);
    }
  };

  const handlePickTicket = async () => {
    setLoading(true);
    try {
      await client.patch(`/tickets/${ticket.id}/pick/`);
      onRefresh();
      onClose();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to pick ticket');
    } finally {
      setLoading(false);
    }
  };

  if (!ticket) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="glass"
            style={{ width: '100%', maxWidth: '450px', padding: '2rem', borderRadius: '24px' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Manage Ticket #{ticket.id}</h2>
              <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-dim)', marginBottom: '0.5rem' }}>Current Status: {ticket.status}</p>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>{ticket.title}</h3>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <select 
                  style={{
                    flex: 1,
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid var(--glass-border)',
                    padding: '0.75rem',
                    borderRadius: '10px',
                    color: 'white'
                  }}
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  <option value="OPEN">Open</option>
                  <option value="ASSIGNED">Assigned</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="RESOLVED">Resolved</option>
                  <option value="CLOSED">Closed</option>
                </select>
                <button onClick={handleUpdateStatus} disabled={loading} className="btn btn-primary">
                  Update
                </button>
              </div>

              {!ticket.assigned_to && (
                <button onClick={handlePickTicket} disabled={loading} className="btn" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', justifyContent: 'center' }}>
                  <UserPlus size={18} />
                  Self Assign (Pick)
                </button>
              )}

              <button className="btn" style={{ background: 'rgba(99, 102, 241, 0.1)', color: '#818cf8', justifyContent: 'center' }}>
                <MessageSquare size={18} />
                Add Comment
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default ActionModal;
