import React, { useState } from 'react';
import client from '../api/client';
import { X, Save } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const TicketModal = ({ isOpen, onClose, onRefresh }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'MEDIUM'
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await client.post('/tickets/', formData);
      onRefresh();
      onClose();
      setFormData({ title: '', description: '', priority: 'MEDIUM' });
    } catch (err) {
      console.error(err);
      alert('Failed to create ticket. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

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
            style={{ width: '100%', maxWidth: '500px', padding: '2rem', borderRadius: '24px' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>New Service Request</h2>
              <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <label style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>Summary</label>
                <input 
                  type="text" 
                  placeholder="Brief title of the issue"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <label style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>Description</label>
                <textarea 
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid var(--glass-border)',
                    padding: '0.75rem 1rem',
                    borderRadius: '10px',
                    color: 'white',
                    outline: 'none',
                    minHeight: '100px',
                    fontFamily: 'inherit'
                  }}
                  placeholder="Provide detailed information..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  required
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <label style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>Priority Level</label>
                <select 
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid var(--glass-border)',
                    padding: '0.75rem 1rem',
                    borderRadius: '10px',
                    color: 'white',
                    outline: 'none'
                  }}
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: e.target.value})}
                >
                  <option value="LOW">Low - General Inquiry</option>
                  <option value="MEDIUM">Medium - Performance Issue</option>
                  <option value="HIGH">High - Service Disruption</option>
                  <option value="CRITICAL">Critical - System Down</option>
                </select>
              </div>

              <button disabled={loading} type="submit" className="btn btn-primary" style={{ justifyContent: 'center', marginTop: '1rem' }}>
                <Save size={20} />
                {loading ? 'Creating...' : 'Submit Request'}
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default TicketModal;
