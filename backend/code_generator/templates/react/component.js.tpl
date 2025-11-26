import React from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';

const {{ component_name }} = ({ 
  className = '',
  children,
  variant = 'default',
  ...props 
}) => {
  const baseClasses = '{{ base_classes }}';
  
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50',
    default: 'bg-white text-gray-900 shadow-sm hover:bg-gray-50',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${className}`.trim();

  return (
    <motion.div
      className={classes}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      {...props}
    >
      {children}
    </motion.div>
  );
};

{{ component_name }}.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'outline', 'default']),
};

export default {{ component_name }};