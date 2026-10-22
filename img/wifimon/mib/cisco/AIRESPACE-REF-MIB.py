#
# PySNMP MIB module AIRESPACE-REF-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file://.\mib_files\sources\AIRESPACE-REF-MIB
# Produced by pysmi-0.3.4 at Tue Aug 13 17:53:33 2024
# On host ? platform ? version ? by user ?
# Using Python version 3.10.14 | packaged by Anaconda, Inc. | (main, May  6 2024, 19:44:50) [MSC v.1916 64 bit (AMD64)]
#
ObjectIdentifier, OctetString, Integer = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ValueSizeConstraint", "SingleValueConstraint", "ConstraintsUnion", "ValueRangeConstraint")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
Counter64, NotificationType, Counter32, Unsigned32, IpAddress, iso, enterprises, ModuleIdentity, Bits, ObjectIdentity, MibIdentifier, Gauge32, Integer32, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn = mibBuilder.importSymbols("SNMPv2-SMI", "Counter64", "NotificationType", "Counter32", "Unsigned32", "IpAddress", "iso", "enterprises", "ModuleIdentity", "Bits", "ObjectIdentity", "MibIdentifier", "Gauge32", "Integer32", "TimeTicks", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
airespace = ModuleIdentity((1, 3, 6, 1, 4, 1, 14179))
airespace.setRevisions(('2005-12-19 00:00',))
if mibBuilder.loadTexts: airespace.setLastUpdated('200512190000Z')
if mibBuilder.loadTexts: airespace.setOrganization('Airespace, Inc.')
mibBuilder.exportSymbols("AIRESPACE-REF-MIB", airespace=airespace, PYSNMP_MODULE_ID=airespace)
