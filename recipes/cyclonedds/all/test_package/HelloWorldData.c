/****************************************************************

  Generated by Eclipse Cyclone DDS IDL to C Translator
  File name: HelloWorldData.c
  Source: /home/scotthinton/git/conan-center-index/recipes/cyclonedds/all/test_package/HelloWorldData.idl
  Cyclone DDS: V0.10.3

*****************************************************************/
#include "HelloWorldData.h"

static const uint32_t HelloWorldData_Msg_ops [] =
{
  /* Msg */
  DDS_OP_ADR | DDS_OP_FLAG_KEY | DDS_OP_FLAG_MU | DDS_OP_TYPE_4BY | DDS_OP_FLAG_SGN, offsetof (HelloWorldData_Msg, userID),
  DDS_OP_ADR | DDS_OP_TYPE_STR, offsetof (HelloWorldData_Msg, message),
  DDS_OP_RTS,
  
  /* key: userID */
  DDS_OP_KOF | 1, 0u /* order: 0 */
};

static const dds_key_descriptor_t HelloWorldData_Msg_keys[1] =
{
  { "userID", 5, 0 }
};

/* Type Information:
  [MINIMAL 6e42149eb141a0d72594c650d73c] (#deps: 0)
  [COMPLETE b1a3b1fb8b1a60516014297c3b8a] (#deps: 0)
*/
#define TYPE_INFO_CDR_HelloWorldData_Msg (unsigned char []){ \
  0x60, 0x00, 0x00, 0x00, 0x01, 0x10, 0x00, 0x40, 0x28, 0x00, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, \
  0x14, 0x00, 0x00, 0x00, 0xf1, 0x6e, 0x42, 0x14, 0x9e, 0xb1, 0x41, 0xa0, 0xd7, 0x25, 0x94, 0xc6, \
  0x50, 0xd7, 0x3c, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, \
  0x00, 0x00, 0x00, 0x00, 0x02, 0x10, 0x00, 0x40, 0x28, 0x00, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, \
  0x14, 0x00, 0x00, 0x00, 0xf2, 0xb1, 0xa3, 0xb1, 0xfb, 0x8b, 0x1a, 0x60, 0x51, 0x60, 0x14, 0x29, \
  0x7c, 0x3b, 0x8a, 0x00, 0x66, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, \
  0x00, 0x00, 0x00, 0x00\
}
#define TYPE_INFO_CDR_SZ_HelloWorldData_Msg 100u
#define TYPE_MAP_CDR_HelloWorldData_Msg (unsigned char []){ \
  0x4c, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0xf1, 0x6e, 0x42, 0x14, 0x9e, 0xb1, 0x41, 0xa0, \
  0xd7, 0x25, 0x94, 0xc6, 0x50, 0xd7, 0x3c, 0x00, 0x34, 0x00, 0x00, 0x00, 0xf1, 0x51, 0x01, 0x00, \
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, \
  0x0b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0x00, 0x04, 0x58, 0x5c, 0x95, 0x70, 0x00, \
  0x0c, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x70, 0x00, 0x78, 0xe7, 0x31, 0x02, \
  0x7a, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0xf2, 0xb1, 0xa3, 0xb1, 0xfb, 0x8b, 0x1a, 0x60, \
  0x51, 0x60, 0x14, 0x29, 0x7c, 0x3b, 0x8a, 0x00, 0x62, 0x00, 0x00, 0x00, 0xf2, 0x51, 0x01, 0x00, \
  0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x48, 0x65, 0x6c, 0x6c, \
  0x6f, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x44, 0x61, 0x74, 0x61, 0x3a, 0x3a, 0x4d, 0x73, 0x67, 0x00, \
  0x3a, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, \
  0x31, 0x00, 0x04, 0x00, 0x07, 0x00, 0x00, 0x00, 0x75, 0x73, 0x65, 0x72, 0x49, 0x44, 0x00, 0x00, \
  0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x70, 0x00, \
  0x08, 0x00, 0x00, 0x00, 0x6d, 0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x00, 0x00, 0x00, 0x00, 0x00, \
  0x22, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0xf2, 0xb1, 0xa3, 0xb1, 0xfb, 0x8b, 0x1a, 0x60, \
  0x51, 0x60, 0x14, 0x29, 0x7c, 0x3b, 0x8a, 0xf1, 0x6e, 0x42, 0x14, 0x9e, 0xb1, 0x41, 0xa0, 0xd7, \
  0x25, 0x94, 0xc6, 0x50, 0xd7, 0x3c\
}
#define TYPE_MAP_CDR_SZ_HelloWorldData_Msg 246u
const dds_topic_descriptor_t HelloWorldData_Msg_desc =
{
  .m_size = sizeof (HelloWorldData_Msg),
  .m_align = dds_alignof (HelloWorldData_Msg),
  .m_flagset = DDS_TOPIC_FIXED_KEY | DDS_TOPIC_FIXED_KEY_XCDR2 | DDS_TOPIC_XTYPES_METADATA,
  .m_nkeys = 1u,
  .m_typename = "HelloWorldData::Msg",
  .m_keys = HelloWorldData_Msg_keys,
  .m_nops = 3,
  .m_ops = HelloWorldData_Msg_ops,
  .m_meta = "",
  .type_information = { .data = TYPE_INFO_CDR_HelloWorldData_Msg, .sz = TYPE_INFO_CDR_SZ_HelloWorldData_Msg },
  .type_mapping = { .data = TYPE_MAP_CDR_HelloWorldData_Msg, .sz = TYPE_MAP_CDR_SZ_HelloWorldData_Msg }
};

